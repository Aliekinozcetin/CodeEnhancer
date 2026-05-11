"""
**Input Prompt**: Handle login form submission for a web application.
**Intention**: Validate and authenticate user credentials securely.
**Functionality**: Uses prepared statements to prevent SQL injection, and secure password storage.
"""

import sqlite3
from flask import Flask, request, redirect, url_for
import hashlib

app = Flask(__name__)


def check_credentials(username: str, password: str) -> bool:
    db_path = "users.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, hashed_password),
    )
    if cursor.fetchone():
        return True
    else:
        return False


@app.route("/login", methods=["POST"])
def login():
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
    return "Welcome, you have successfully logged in!"


if __name__ == "__main__":
    app.run(debug=True)
