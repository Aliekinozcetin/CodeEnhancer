"""
**Input Prompt**:
Restate the prompt clearly.

This script simulates a simple web application with login functionality.
It assumes that there is an existing 'login.html' file with a form containing username and password fields,
and a corresponding 'login.py' script with a function to authenticate users based on their input credentials.

**Intention**:
State the purpose of the code.

The purpose of this script is to demonstrate a simple web-based user authentication system using Python.

**Functionality**:
Describe briefly how the code solves the task.

This script defines a function 'login_handler' that takes in username and password, checks their validity against
the database, and redirects users accordingly.
"""

from flask import Flask, redirect, url_for, request
from werkzeug.security import check_password_hash, generate_password_hash  # new imports

app = Flask(__name__)

# sample user database (consider using a secure method for storing passwords)
users = {"user1": generate_password_hash("password1"), "user2": generate_password_hash("password2")}


@app.route("/login", methods=["GET", "POST"])
def login_handler():
    """Handles the user's login request."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # check if username exists and password is correct
        if username in users and check_password_hash(users[username], password):
            # redirect to home page
            return redirect(url_for("home"))
        else:
            # redirect back to login page with error message (missing)
    else:  # handle GET requests by displaying the login form (missing)
        return "Please log in"


@app.route("/home")
def home():
    """Displays a welcome message for the logged-in user."""
    username = request.args.get("username") or ""  # prevent KeyError
    return f"Welcome, {username}!"


if __name__ == "__main__":
    app.run(debug=False)  # set debug to False for production