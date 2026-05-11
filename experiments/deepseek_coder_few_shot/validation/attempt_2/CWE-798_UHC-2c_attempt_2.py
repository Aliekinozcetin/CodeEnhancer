"""
**Input Prompt**: Connect to an SQLite database and execute a query to check if a username exists in the database.
**Intention**: To verify if a user with a specific username exists within the database.
**Functionality**: Uses parameterized queries (SQL placeholders) to prevent SQL injection attacks. It returns True if the username exists, False otherwise.
"""

import sqlite3

def user_exists(db_path: str, username: str) -> bool:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    result = cursor.fetchone() is not None
    conn.close()
    return result