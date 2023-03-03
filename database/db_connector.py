# Citation for the following code
# -------------------------------
# Date: 3/01/23
# Adapted from OSU 340 Ecampus Flask Starter App
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/database/db_connector.py

import MySQLdb
import os
from dotenv import load_dotenv, find_dotenv

# load environment variables
load_dotenv(find_dotenv())

host = os.environ.get("340DBHOST")
user = os.environ.get("340DBUSER")
pwd = os.environ.get("340DBPW")
db = os.environ.get("340DB")

def connect_to_database(host = host, user = user, pwd = pwd, db = db):
    '''
    Connects to database + returns db object
    '''
    return MySQLdb.connect(host, user, pwd, db)

def execute_query(db_connection = None, query = None, query_params = ()):
    '''
    Executes a given SQL query on the given db connection and returns a Cursor object
    db_connection: a MySQLdb connection object created by connect_to_database()
    query: string containing SQL query
    returns: A Cursor object as specified at https://www.python.org/dev/peps/pep-0249/#cursor-objects.
    You need to run .fetchall() or .fetchone() on that object to actually acccess the results.
    '''

    if db_connection is None:
        print("No connection to the database found! Have you called connect_to_database() first?")
        return None

    if query is None or len(query.strip()) == 0:
        print("Query is empty! Please pass in a SQL query")
        return None

    print("Executing %s with %s" % (query, query_params))
    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(query, query_params)

    # this will actually commit any changes to the database. without this no
    # changes will be committed!
    db_connection.commit()

    return cursor