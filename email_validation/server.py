from flask import (Flask, render_template, redirect, request, session, flash)
from mysqlconnection import connectToMySQL
import re
from datetime import datetime  

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
app.secret_key = 'unicorn'
mysql = connectToMySQL('emails')

users = mysql.query_db("SELECT * FROM user;") 

@app.route('/')
def index():
    # print("muhhh")
    return render_template('index.html')

@app.route('/submit', methods=["POST"])
def check_emailExists():
    # print("------khkjhkjhk--")
    for user in users:
        if request.form['email'] == user['email']:
            flash('Email already exists')
            return redirect('/')

    if len(request.form['email']) < 1:
        flash('Email can not be blank', 'message')
        return redirect('/')

    elif not EMAIL_REGEX.match(request.form['email']):
        flash('Invalid email address', 'message')
        return redirect('/')

    else: 
        add_query = "INSERT INTO user (email, created_at, updated_at) VALUES(%(email)s, NOW(), NOW());"
        data = {
            'email': request.form['email'],
            'created_at': datetime.now()
        }
        mysql.query_db(add_query, data)
        return redirect('/added')
    
@app.route('/added')
def success():
    userMail = mysql.query_db("SELECT email, created_at, updated_at FROM user;")
    return render_template('success.html', userMail = userMail)

if __name__ == "__main__":
    app.run(debug = True)