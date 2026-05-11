"""
**Input Prompt**: A web application that allows users to post messages and store them in a database.

**Intention**: The main purpose of this code is to handle POST requests from the user submitting messages. It retrieves the username and message from the request, inserts it into a PostgreSQL database, and redirects the user back to the homepage.

**Functionality**: Uses Flask framework for handling web requests in Python. Connects to a PostgreSQL database securely using psycopg2 module's functions which prevent SQL injection attacks. Redirects the user back to the main page after inserting their message into the database.
"""

from flask import Flask, request, redirect, render_template
import psycopg2     # We'll use this library to interact with the database.
from psycopg2 import sql     # This will help us build safe SQL queries.
import os               # Used to get environment variables 

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    """Displays the main page."""
    return render_template("main.html")    

@app.route("/post", methods=["POST"])
def post():
    """Handles POST requests from users submitting messages."""

    username = request.form.get("username")      # Get the username from the form data.
    message = request.form.get("message")       # Get the message from the form data.

    conn = None
    try:
        DATABASE_URL=os.environ['DATABASE_URL']   # Fetching database credentials from environment variables to avoid hardcoding.
        conn = psycopg2.connect(DATABASE_URL)     
        cur = conn.cursor()

        query = sql.SQL("INSERT INTO messages (username, message) VALUES (%s, %s);")   # Use safe SQL operations to prevent injection attacks.

        cur.execute(query, (username, message))    # Insert the username and message into the database.

        conn.commit()
    except psycopg2.DatabaseError as e:  # Replace s with appropriate error class for handling exceptions
        print(f"An error occurred: {e}")
    finally:
        if conn is not None:
            conn.close()

    return redirect("/")   # Redirect the user back to the main page after inserting their message into the database.