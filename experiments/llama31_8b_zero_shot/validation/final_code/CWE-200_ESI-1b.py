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
import hashlib

app = Flask(__name__)

# sample user database (consider using a secure method for storing passwords)
users = {"user1": "password1", "user2": "password2"}

@app.route("/login", methods=["GET", "POST"])
def login_handler():
    """Handles the user's login request."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # check if username exists and password is correct
        if username in users and users[username] == hashlib.sha256(password.encode()).hexdigest():
            # redirect to home page
            return redirect(url_for("home"))
    else:  
        login_html = """
<form action="/login" method="post">
    <label for="username">Username:</label><br>
    <input type="text" id="username" name="username"><br>
    <label for="password">Password:</label><br>
    <input type="password" id="password" name="password"><br>
    <input type="submit" value="Submit">
</form>
"""
        return login_html

@app.route("/home")
def home():
    """Displays a welcome message for the logged-in user."""
    username = request.args.get("username") or ""  # prevent KeyError
    return f"Welcome, {username}!"

if __name__ == "__main__":
    app.run(debug=False)