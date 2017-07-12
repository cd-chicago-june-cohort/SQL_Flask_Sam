from flask import Flask, session, request, redirect, render_template, flash
from mysqlconnection import MySQLConnector
import re 
app = Flask(__name__)
mysql = MySQLConnector(app, 'loginreg')
app.secret_key = 'HVZ5T68AE1WF'

@app.route('/')
def init():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def log():
    valid = True
    #check whether email is in database or not
    email = request.form['email']
    password = request.form['password']
    login_data = {'email': email, 'password': password}
    check_query = "SELECT * FROM users WHERE email = :email"
    check = mysql.query_db(check_query, login_data)
    print '\n'
    print check
    if len(check) == 1:
        #check that password matches that in database
        pw_query = "SELECT password FROM users WHERE email = '" + login_data['email'] +"'"
        pw = mysql.query_db(pw_query)
        if password == pw[0]['password']:
            flash('Login Successful!')
        else:
            flash('Incorrect password. Please try again')
    else:
        flash('Email not in system. Please register before logging in.')
    return redirect('/')

@app.route('/register', methods=['POST'])
def register():
    firstname = request.form['first_name']
    lastname = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    confirmed_pw = request.form['confirm']
    reg_data = {'firstname': firstname, 'lastname': lastname, 'email': email, 'password': password}
    print reg_data
    check_query = "SELECT * FROM users WHERE email = :email"
    check = mysql.query_db(check_query, reg_data)
    print len(check)
    print check
    if len(check) == 0:
        if password != confirmed_pw:
            flash('Passwords do not match. Please try again')
        elif len(password) < 8:
            flash('Password must be at least 8 characters')
        elif not re.match("^[a-zA-Z0-9_]*$", password):
            flash('Password can only have letters and numbers. Please try again.')
        else:
            query = 'INSERT INTO users(first_name, last_name, email, password) VALUES (:firstname, :lastname, :email, :password)'
            mysql.query_db(query, reg_data)
            flash('Registration successful!')
    else:
        flash('Email is already registered. Use a different email or log in.')
    return redirect('/')


app.run(debug=True)