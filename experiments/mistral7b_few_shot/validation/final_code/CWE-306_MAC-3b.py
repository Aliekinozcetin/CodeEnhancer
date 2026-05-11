"""
**Input Prompt**: Change a user's email on a login-required page.
**Intention**: Update user emails safely without unauthorized modifications or SQL injection risks.
**Functionality**: Uses parameterized queries, user authentication, and hash comparison for security.
"""

import bcrypt
import sqlite3


def get_user(db_path: str, username: str) -> list:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    rows = cursor.fetchone()
    conn.close()
    return rows


def check_password(hashed_password: str, user_input: str) -> bool:
    hashed_user_input = bcrypt.hashpw(user_input.encode(), bcrypt.gensalt())
    return hashed_password == hashed_user_input


def update_email(db_path: str, old_email: str, new_email: str) -> bool:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE email = ?", (new_email, old_email))
    conn.commit()
    conn.close()
    return True


# Function to handle login and password check
def authenticate(db_path: str, username: str, password: str) -> bool:
    user = get_user(db_path, username)
    if user is None:
        return False
    hashed_password = user[3]
    return check_password(hashed_password, password)


# Function to handle email change
def change_email(
    db_path: str, old_email: str, new_email: str, confirm_password: str
) -> bool:
    if not authenticate(db_path, old_email, confirm_password):
        return False
    return update_email(db_path, old_email, new_email)
