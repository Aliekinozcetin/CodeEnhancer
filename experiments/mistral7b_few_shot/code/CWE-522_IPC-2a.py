"""
**Input Prompt**: Hash a password and store it in a SQLite database along with the username.
**Intention**: Store sensitive information securely in the database.
**Functionality**: Uses bcrypt for password hashing, parameterized queries to prevent SQL injection.
"""

import bcrypt
import sqlite3


def create_user(db_path: str, username: str, password: str) -> None:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, hashed_password),
    )
    conn.commit()
    conn.close()
