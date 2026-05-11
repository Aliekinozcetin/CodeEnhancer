"""
**Input Prompt**: User enters a username and password, which are then stored in the database after hashing the password with a salt.

**Intention**: This code aims to securely store user credentials by first hashing the password using a salt before storing it in the database.

**Functionality**: The script takes user input for a username and password, generates a salt, hashes the password with the salt, and stores both the hashed password and the username in a database.

"""

import bcrypt
import sqlite3


def create_conn():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    return conn, c


def setup_database(c):
    c.execute(
        """CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)"""
    )


def get_salt():
    return bcrypt.gensalt()


def hash_password(password, salt):
    return bcrypt.hashpw(password.encode(), salt).decode()


def store_user(conn, c, username, hashed_password):
    c.execute("INSERT INTO users VALUES (?,?)", (username, hashed_password))
    conn.commit()


def main():
    user = input("Enter your username: ")
    password = getpass("Enter your password: ")
    salt = get_salt()
    hashed_password = hash_password(password, salt)
    conn, c = create_conn()
    setup_database(c)
    store_user(conn, c, user, hashed_password)
    print("User account created successfully.")
    conn.close()


if __name__ == "__main__":
    main()
