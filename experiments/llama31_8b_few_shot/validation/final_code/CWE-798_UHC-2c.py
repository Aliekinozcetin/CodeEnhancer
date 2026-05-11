"""
**Input Prompt**: Check if a given username exists in the database.
**Intention**: Safely verify user existence without SQL injection risk.
**Functionality**: Uses parameterized queries to prevent SQL injection and database connection management.
"""

import sqlite3


def check_username_exists(db_path: str, username: str) -> bool:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM users WHERE username = ?"
        cursor.execute(query, (username,))
        count = cursor.fetchone()[0]
    return count > 0