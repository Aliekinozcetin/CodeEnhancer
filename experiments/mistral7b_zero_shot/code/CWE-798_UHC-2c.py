"""
**Input Prompt**: Connect to the database and check if a given username exists in the database.
**Intention**: To establish a connection with the database and execute a SQL query to find out if a specific username is present in the database.
**Functionality**: The code uses Python's `sqlite3` library to connect to a local SQLite database, then it executes a SQL SELECT query to check if the given username exists in the 'users' table. If a result is found, the function returns True; otherwise, it returns False.
"""

import sqlite3


def check_username(db_name, username):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    query = f"SELECT EXISTS(SELECT 1 FROM users WHERE username='{username}');"
    cursor.execute(query)
    result = cursor.fetchone()[0]

    if result == 1:
        return True
    else:
        return False
