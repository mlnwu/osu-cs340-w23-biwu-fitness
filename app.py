# Citation for the following code
# -------------------------------
# Date: 3/01/23
# Adapted from OSU 340 Ecampus Flask Starter App
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/app.py

from flask import Flask, render_template, redirect, url_for, request
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv, find_dotenv

# load environment variables
load_dotenv(find_dotenv())

host = os.environ.get("340DBHOST")
user = os.environ.get("340DBUSER")
pwd = os.environ.get("340DBPW")
db_name = os.environ.get("340DB")

# Config

app = Flask(__name__)
app.config["MYSQL_HOST"] = host
app.config["MYSQL_USER"] = user
app.config["MYSQL_PASSWORD"] = pwd
app.config["MYSQL_DB"] = db_name
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

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
        cursor = mysql.connection.cursor()
        cursor.execute(query)
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
            cursor = mysql.connection.cursor()
            cursor.execute(query, query_params)
            mysql.connection.commit()

        return redirect(url_for('members'))

@app.route('/edit_member/<int:member_id>', methods=["POST", "GET"])
def edit_member(member_id):
    if request.method == "GET":
        # query to get info of member to be edited
        info_query = "SELECT * FROM Members WHERE member_id = %s"
        cursor = mysql.connection.cursor()
        cursor.execute(query, (member_id,))
        member_data = cursor.fetchall()

        # render edit_member page with specific member info
        return render_template("edit_member.html", member_data=member_data, name="hello")

    if request.method == "POST":

        if request.form:
            # get form inputs
            first_name = request.form["fname"]
            last_name = request.form["lname"]
            tier_type = request.form["tiertype"]
            phone_number = request.form["phone"]
            email = request.form["email"]
            query_params = (first_name, last_name, tier_type, phone_number, email, member_id)

            # write query (no NULL inputs allowed)
            query = "UPDATE Members SET first_name = %s, last_name = %s, tier_type = %s, phone_number = %s, email = %s WHERE member_id = %s"
            cursor = mysql.connection.cursor()
            cursor.execute(query, query_params)
            mysql.connection.commit()
        
        return redirect(url_for('members'))
    

@app.route('/delete_member/<int:member_id>')
def delete_member(member_id):
    # query to delete member with passed id
    query = "DELETE FROM Members WHERE member_id = '%s';"
    cursor = mysql.connection.cursor()
    cursor.execute(query, (member_id,))
    mysql.connection.commit()

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