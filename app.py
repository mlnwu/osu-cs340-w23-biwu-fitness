# Citation for the following code
# -------------------------------
# Date: 3/01/23
# Adapted from OSU 340 Ecampus Flask Starter App
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/app.py

from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv, find_dotenv

import logging

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

@app.route('/classes', methods=["POST", "GET"])
def classes():
    if request.method == "GET":
        # mySQL query to get all classes
        query = "SELECT * FROM Classes"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        classes_data = cursor.fetchall()

        # render classes.html with Classes data
        return render_template("classes.html", classes_data=classes_data)

    if request.method == "POST":
        # get info from Add New Class form

        if request.form:
            # get form inputs
            class_type = request.form["classtype"]
            trainer_id = request.form["trainername"]
            day_scheduled = request.form["weekday"]
            start_time = request.form["starttime"]
            end_time = request.form["endtime"]
            query_params = (class_type, trainer_id, day_scheduled, start_time, end_time)

            # write query
            query = "INSERT INTO Classes (class_type, trainer_id, day_scheduled, start_time, end_time) VALUES (%s, %s, %s, %s, %s);"
            cursor = mysql.connection.cursor()
            cursor.execute(query, query_params)
            mysql.connection.commit()

            return redirect(url_for('classes'))

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
        cursor.execute(info_query, (member_id,))
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
    

@app.route('/trainers', methods=["POST", "GET"])
def trainers():
    if request.method == "GET":
        # mySQL query to get all trainers
        query = "SELECT * FROM Trainers"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        trainer_data = cursor.fetchall()

        # render trainers.html with Trainers data
        return render_template("trainers.html", trainer_data=trainer_data)

    if request.method == "POST":
        # get info from Register New Trainer form

        if request.form:
            # get form inputs
            first_name = request.form["fname"]
            last_name = request.form["lname"]
            phone_number = request.form["phone"]
            email = request.form["email"]
            query_params = (first_name, last_name, phone_number, email)

            # write query (no NULL inputs allowed)
            query = "INSERT INTO Trainers (first_name, last_name, phone_number, email) VALUES (%s, %s, %s, %s);"
            cursor = mysql.connection.cursor()
            cursor.execute(query, query_params)
            mysql.connection.commit()

        return redirect(url_for('trainers'))

@app.route('/edit_trainer/<int:trainer_id>', methods=["POST", "GET"])
def edit_trainer(trainer_id):
    if request.method == "GET":
        # query to get info of trainer to be edited
        info_query = "SELECT * FROM Trainers WHERE trainer_id = %s"
        cursor = mysql.connection.cursor()
        cursor.execute(info_query, (trainer_id,))
        trainer_data = cursor.fetchall()

        # render edit_trainer page with specific trainer info
        return render_template("edit_trainer.html", trainer_data=trainer_data)

    if request.method == "POST":

        if request.form:
            # get form inputs
            first_name = request.form["fname"]
            last_name = request.form["lname"]
            phone_number = request.form["phone"]
            email = request.form["email"]
            query_params = (first_name, last_name, phone_number, email, trainer_id)

            # write query (no NULL inputs allowed)
            query = "UPDATE Trainers SET first_name = %s, last_name = %s, phone_number = %s, email = %s WHERE trainer_id = %s"
            cursor = mysql.connection.cursor()
            cursor.execute(query, query_params)
            mysql.connection.commit()
        
        return redirect(url_for('trainers'))
    

@app.route('/delete_trainer/<int:trainer_id>')
def delete_trainer(trainer_id):
    # query to delete trainer with passed id
    query = "DELETE FROM Trainers WHERE trainer_id = '%s';"
    cursor = mysql.connection.cursor()
    cursor.execute(query, (trainer_id,))
    mysql.connection.commit()

    return redirect(url_for('trainers'))

# dynamically populates dropdown menu for member ids
@app.route('/get_member_names')
def get_member_names():
    # MySQL query to fetch all member ids and names from Members table
    query = "SELECT member_id, first_name, last_name FROM Members;"
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()

    # extract member ids and names from the query result
    member_names = [[row["member_id"], row["first_name"] + " " + row["last_name"]] for row in result]
    print(member_names)
    # return member ids and names in JSON format
    return jsonify(member_names)

# dynamically populates dropdown menu for trainer names
@app.route('/get_trainer_names')
def get_trainer_names():
    # mySQL query to get all trainer ids and first and last names from Trainers table
    query = "SELECT trainer_id, first_name, last_name FROM Trainers;"
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()

    # extract trainer ids and names from result
    trainer_names = [[row["trainer_id"], row["first_name"] + " " + row["last_name"]] for row in result]
    # return trainer ids and names in JSON format
    return jsonify(trainer_names)

@app.route('/transactions', methods=["POST", "GET"])
def transactions():
    if request.method == "GET":
        # mySQL query to get all transactions
        query = "SELECT * FROM Transactions"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        transactions_data = cursor.fetchall()

        # mySQL query to get all membership transaction history
        query = "SELECT * FROM Members_has_Transactions"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        membership_transaction_data = cursor.fetchall()

        # render transaction.html with Transaction data
        return render_template("transactions.html", transactions_data=transactions_data, membership_transaction_data=membership_transaction_data)

    if request.method == "POST":
        # get info from Record a New Membership Transaction form
        member_id = request.form["membername"]
        transaction_amount = request.form["tamount"]
        transaction_date = request.form["tdate"]

        # write query to insert transaction into Transactions table
        query = "INSERT INTO Transactions (members_member_id, transaction_amount, transaction_date) VALUES (%s, %s, %s)"
        cursor = mysql.connection.cursor()
        cursor.execute(query, (member_id, transaction_amount, transaction_date))
        mysql.connection.commit()

        # get transaction_id of newly inserted transaction
        transaction_id = cursor.lastrowid

        # insert transaction into Transactions History table
        query = "INSERT INTO Members_has_Transactions (transactions_transaction_id, members_member_id) VALUES (%s, %s)"
        cursor = mysql.connection.cursor()
        cursor.execute(query, (transaction_id, member_id))
        mysql.connection.commit()

        return redirect(url_for("transactions"))


# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 29901))
    app.run(port=port)