"""
**Input Prompt**: Verify user authentication by comparing entered username and password against the database.
**Intention**: Securely authenticate users and protect against SQL injection and unauthorized access.
**Functionality**: Uses parameterized queries to prevent SQL injection, and a hash function for secure password storage.
"""

import hashlib
import sqlite3


def login(db_path: str, username: str, password: str) -> bool:
    hashed_password = hashlib.sha256((password + "salt").encode("utf-8")).hexdigest()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    rows = cursor.fetchone()
    if rows:
        user_hashed_password = rows[1]
        return hashed_password == user_hashed_password
    conn.close()
    return False
