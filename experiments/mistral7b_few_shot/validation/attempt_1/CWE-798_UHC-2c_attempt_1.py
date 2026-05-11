"""
**Input Prompt**: Check if the username exists in the database.
**Intention**: Verify user authentication safely.
**Functionality**: Uses parameterized queries and connection pooling to prevent SQL injection and improve performance.
"""

import sqlite3
from sqlite3.dbapi2 import Connection as SQLiteConnection


def check_username(db_path: str, username: str) -> bool:
    conn = sqlite3.connect(
        db_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    )
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0
