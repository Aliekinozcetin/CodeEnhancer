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

app = Flask(__name__)

# sample user database
users = {"user1": "password1", "user2": "password2"}


@app.route("/login", methods=["GET", "POST"])
def login_handler():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            # redirect to home page
            return redirect(url_for("home"))
        else:
            # redirect back to login page
            return redirect(url_for("login"))


@app.route("/home")
def home():
    return "Welcome, {}!".format(request.args.get("username"))


if __name__ == "__main__":
    app.run(debug=True)
