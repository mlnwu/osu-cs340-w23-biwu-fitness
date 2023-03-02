from flask import Flask, render_template, redirect, url_for
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

@app.route('/members')
def members():
    return render_template("members.html")

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