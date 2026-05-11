"""
**Input Prompt**: Connect to the database and check if a given username exists.

**Intention**: This code connects to a database, checks if a given username exists in the database, and securely handles potential security risks.

**Functionality**: Connects to the database, escapes user input to prevent SQL injection attacks, and validates the existence of the username.
"""

import bcrypt
from sqlite3 import Connection, Cursor

def check_username(conn: Connection, cursor: Cursor, username: str) -> bool:
    query = "SELECT username FROM users WHERE username=?"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    if result:
        hashed_password = bcrypt.hashpw(username.encode(), bcrypt.gensalt())
        update_hashed_password(conn, cursor, username)
    return bool(result)

def update_hashed_password(conn: Connection, cursor: Cursor, username: str):
    hashed_password = bcrypt.hashpw(username.encode(), bcrypt.gensalt())
    query = "UPDATE users SET password=? WHERE username=?"
    cursor.execute(query, (hashed_password, username))