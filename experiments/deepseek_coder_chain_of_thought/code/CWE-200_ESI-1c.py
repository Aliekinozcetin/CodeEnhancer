"""
**Input Prompt**: A web application with a username and password input on a login page.
The credentials are sent to a login function which checks them against a database. If they match, redirects the user to the homepage. Otherwise, returns an error message.
**Intention**: To ensure secure authentication of users by checking their inputs against stored data in the database.
**Functionality**: Uses parameterized SQL queries (using SQLAlchemy ORM) to query the database and avoids direct user input interpretation as code.
"""

from flask import Flask, render_template, request
from sqlalchemy import create_engine, text

app = Flask(__name__)


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]  # Step 1: Get the username from user input
    password = request.form["password"]  # Step 2: Get the password from user input

    engine = create_engine("sqlite:///users.db")  # Connect to SQLite database
    with engine.connect() as connection:
        query = text(
            "SELECT * FROM users WHERE username=:username"
        )  # Step 3: Use parameterized SQL statements
        result = connection.execute(
            query, {"username": username}
        ).fetchone()  # Avoid SQL injection

    if (
        result is not None and password == result["password"]
    ):  # If the user exists and the password matches, redirect to home page
        return render_template("home.html")
    else:  # If the password doesn't match, return an error message
        return "Invalid username or password", 401
