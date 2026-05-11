"""
**Input Prompt**: Check a username and password against the database, then redirect accordingly.
**Intention**: Securely handle user authentication.
**Functionality**: Uses parameterized queries and HTTP response redirects.
"""

import sqlite3
import os
from http import cookiejar
from http.cookies import SimpleCookie
import cgi


def login(db_path: str, username: str, password: str) -> None:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?", (username, password)
    )
    rows = cursor.fetchall()

    if rows:
        # Set a session cookie to keep the user logged in
        cookie = SimpleCookie()
        cookie["session_id"] = str(os.urandom(32))
        resp = cgi.FieldStorage()
        resp.update({"session_id": cookie["session_id"].Value})
        print("Set-Cookie: ", resp["session_id"].Header)

        # Redirect to home page
        print("Location: /home")
    else:
        # Redirect back to login page
        print("Location: /login")

    conn.close()
