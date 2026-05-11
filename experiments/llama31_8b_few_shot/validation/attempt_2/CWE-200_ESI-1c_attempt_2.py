"""
**Input Prompt**: Login into the system with a provided username and password.
**Intention**: Authenticate users securely without exposing passwords or storing them in plaintext.
**Functionality**: Uses parameterized queries to prevent SQL injection, stores passwords hashed using bcrypt.
"""

import sqlite3
from flask import redirect, url_for
import bcrypt

# Hashing salt for bcrypt
salt = bcrypt.gensalt()


def login(username: str, password: str) -> bool:
    db_path = "database.db"

    # Connect to the SQLite database. This will create a new database if it doesn't exist.
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query the database for the username and retrieve the hashed password
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()

    if row:
        stored_password_hash = row[0]

        # Compare the provided password to the hashed password using bcrypt.compare
        if bcrypt.checkpw(password.encode("utf-8"), stored_password_hash):
            conn.close()
            return True  # Successful login, redirect user

    conn.close()
    return False


def authenticate_user(username: str, password: str) -> bool:
    try:
        is_authenticated = login(username, password)

        if is_authenticated:
            # Successful login, redirect to home page
            return redirect(url_for("home"))

    except Exception as e:
        print(f"An error occurred during authentication: {e}")

    return False