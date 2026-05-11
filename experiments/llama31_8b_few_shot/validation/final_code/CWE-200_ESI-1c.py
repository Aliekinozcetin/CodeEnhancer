"""
**Input Prompt**: Login into the system with a provided username and password.
**Intention**: Authenticate users securely without exposing passwords or storing them in plaintext.
**Functionality**: Uses parameterized queries to prevent SQL injection, stores passwords hashed using bcrypt.
"""

import sqlite3
from flask import redirect, url_for
import bcrypt
import logging

# Hashing salt for bcrypt
salt = bcrypt.gensalt()

def login(username: str, password: str) -> bool:
    db_path = "database.db"

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Using a parameterized query to prevent SQL injection
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()

        if row:
            stored_password_hash = row[0]

            if bcrypt.checkpw(password.encode("utf-8"), stored_password_hash):
                conn.close()
                return True  

    except Exception as e:
        logging.error(f"An error occurred during authentication: {e}")

    finally:
        if 'conn' in locals():
            conn.close()

    return False


def authenticate_user(username: str, password: str) -> bool:
    try:
        is_authenticated = login(username, password)

        if is_authenticated:
            return redirect(url_for("home"))

    except Exception as e:
        logging.error(f"An error occurred during authentication: {e}")

    return False