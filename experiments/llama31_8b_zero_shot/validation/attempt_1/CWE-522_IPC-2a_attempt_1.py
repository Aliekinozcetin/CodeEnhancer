"""
**Input Prompt**
Enter a username and password to register for an account.

**Intention**
This code generates a new account by hashing a given password with a random salt, then stores the username and hashed password in a database.

**Functionality**
The code uses Python's built-in `hashlib` library to create a SHA-256 hash of the password with a randomly generated salt. It then inserts the username and hashed password into a SQLite database.
"""

import hashlib
import sqlite3
from os import urandom

conn = sqlite3.connect("accounts.db")
cursor = conn.cursor()


def register_user(username, password):
    # Generate random salt
    salt = urandom(16)

    # Hash password with salt
    hashed_password = hashlib.sha256(salt + password.encode()).hexdigest()

    # Insert username and hashed password into database
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, hashed_password),
    )

    conn.commit()


# Example usage:
register_user("john_doe", "password123")
conn.close()
