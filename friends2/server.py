from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'friends_againdb')

@app.route('/')
def index():
    friends = mysql.query_db('SELECT * FROM friends')
    print friends
    return render_template('index.html', friend_list = friends)

@app.route('/addfriends', methods=['POST'])
def new_friend():
    data = {}
    name = request.form['name']
    age = request.form['age']
    data['name'] = name
    data['age'] = age
    print data
    query = 'INSERT INTO friends(name, age, friends_since) VALUES (:name, :age, NOW())'
    mysql.query_db(query, data)
    return redirect('/')

app.run(debug=True)