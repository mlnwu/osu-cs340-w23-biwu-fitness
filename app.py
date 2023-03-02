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

    if request.method == "POST":
        # get info from Add New Member form

        if request.form:
            # get form inputs
            first_name = request.form["fname"]
            last_name = request.form["lname"]
            tier_type = request.form["tiertype"]
            phone_number = request.form["phone"]
            email = request.form["email"]
            query_params = (first_name, last_name, tier_type, phone_number, email)

            # write query (no NULL inputs allowed)
            query = "INSERT INTO Members (first_name, last_name, tier_type, phone_number, email) VALUES (%s, %s, %s, %s, %s);"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_params)

        return redirect(url_for('members'))

@app.route('/delete_member/<int:member_id>')
def delete_member(member_id):
    # query to delete member with passed id
    query = "DELETE FROM Members WHERE member_id = '%s';"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(member_id,))

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