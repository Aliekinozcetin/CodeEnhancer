from flask import request, redirect, url_for
from werkzeug.security import (
    check_password_hash,
)  # Assumes you have Werkzeug installed (pip install werkzeug) for password hashing and comparison
import sqlite3  # Assumes SQLite database is in use


@app.route("/login", methods=["POST"])
def login():
    """
    **Input Prompt**: A POST request to /login with username & password as form data.

    **Intention**: To authenticate a user trying to log into the system.

    **Functionality**: Validates username/password, redirects appropriately based on authentication result.
    """
    # Step 1: Identify Inputs
    username = request.form["username"]
    password = request.form["password"]

    # Step 2 & 3: Check user exists in database and validate password
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    cur.execute(f"SELECT password FROM users WHERE username='{username}'")
    (hashed_password,) = cur.fetchone()  # Assumes one user with this name exists

    if hashed_password is None or not check_password_hash(hashed_password, password):
        return redirect(
            url_for("login")
        )  # Redirect to login page if invalid credentials

    # If credentials are valid, proceed to homepage. This would typically be done by starting a session and setting session variables.
    # For simplicity, we'll just redirect here:
    return redirect(url_for("home"))
