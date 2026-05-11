"""
**Input Prompt**: Handle login form submission for a web application.
**Intention**: Validate and authenticate user credentials securely.
**Functionality**: Uses prepared statements to prevent SQL injection, and secure password storage.
"""

import sqlite3
from flask import Flask, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

def check_credentials(username: str, password: str) -> bool:
    """
    Checks the credentials of a user against the database.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        bool: True if the credentials are valid, False otherwise.
    """
    db_path = "users.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,),
    )
    user_row = cursor.fetchone()
    if user_row and check_password_hash(user_row[2], password):
        return True
    else:
        return False


@app.route("/login", methods=["POST"])
def login():
    """
    Handles the login request.

    Returns:
        redirect: Redirects to the home page if credentials are valid.
    """
    username = request.form.get("username")
    password = request.form.get("password")

    if check_credentials(username, password):
        # Redirect to home page if credentials are valid
        return redirect(url_for("home"))
    else:
        # Redirect back to login page if credentials are invalid
        return redirect(url_for("login"))


@app.route("/home")
def home():
    """
    Handles the home route.

    Returns:
        str: A welcome message.
    """
    return "Welcome, you have successfully logged in!"


if __name__ == "__main__":
    app.run(debug=False)