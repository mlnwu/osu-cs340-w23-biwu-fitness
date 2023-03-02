# Citation for the following code
# -------------------------------
# Date: 3/01/23
# Adapted from OSU 340 Ecampus Flask Starter App
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/app.py

from flask import Flask, render_template, redirect, url_for, request
from flask_mysqldb import MySQL
import os
import database.db_connector as db

# Config

app = Flask(__name__)

db_connection = db.connect_to_database()

# Routes

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/')
def root():
    return redirect(url_for('index'))

@app.route('/classes')
def classes():
    return render_template("classes.html")

@app.route('/members', methods=["POST", "GET"])
def members():
    if request.method == "GET":
        # mySQL query to get all members
        query = "SELECT * FROM Members"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        members_data = cursor.fetchall()

        # render members.html with Members data
        return render_template("members.html", members_data=members_data)

    if request.method == 'POST':
        return redirect(url_for('members'))

@app.route('/trainers')
def trainers():
    return render_template("trainers.html")

@app.route('/transactions')
def transactions():
    return render_template("transactions.html")

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 29901))
    app.run(port=port)