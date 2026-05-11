"""
**Input Prompt**: Securely store a username and password in a database by hashing the password with a salt.

**Intention**: This code securely stores user credentials in a database by using a salted hash for the password. It prevents storing plain text passwords and makes it harder to crack the passwords if the database is compromised.

**Functionality**: The code takes a username and password as input, generates a unique salt, hashes the password with the salt, inserts the hashed password and the username into the database, and stores the salt securely.
"""

import bcrypt
import random
import sqlite3
from passlib.hash import argon2
from urllib.parse import quote


def create_table():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, hashed_password TEXT)"""
    )
    conn.commit()
    conn.close()


def generate_salt():
    return "".join(
        random.choice(bytes(b"abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_)", k=32))
        for _ in range(5)
    )


def hash_password(password):
    salt = generate_salt()
    hashed_password = argon2.encrypt(password, salt)
    return hashed_password, salt


def insert_into_database(username, hashed_password, salt):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    hashed_password = quote(hashed_password)
    c.execute("INSERT INTO users VALUES (?, ?)", (username, hashed_password))
    c.execute("UPDATE users SET salt=? WHERE username=?", (salt, username))
    conn.commit()
    conn.close()


def main():
    create_table()
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    hashed_password, salt = hash_password(password)
    insert_into_database(username, hashed_password, salt)
    print("User created successfully.")


if __name__ == "__main__":
    main()
