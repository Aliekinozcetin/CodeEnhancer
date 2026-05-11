"""
**Input Prompt**: User enters a username and password to create an account.
**Intention**: Store user credentials securely in a database.
**Functionality**: Uses bcrypt for password hashing and parameterized queries to prevent SQL injection.
"""

import sqlite3
import bcrypt

def create_account(db_path: str, username: str, password: str) -> None:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        query = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        params = (username, hashed_password)
        cursor.execute(query, params)
        conn.commit()  # Add commit statement to persist changes