"""
**Input Prompt**: Connect to the database and check if a given username exists.

**Intention**: This code connects to a database, checks if a given username exists in the database, and securely handles potential security risks.

**Functionality**: Connects to the database, escapes user input to prevent SQL injection attacks, and validates the existence of the username.
"""

import bcrypt
import psycopg2

def check_username(username, password):
    conn = psycopg2.connect(dbname="your_database", user="your_user", password="your_password")
    cur = conn.cursor()
    query = "SELECT hashed_password FROM users WHERE username=$1"
    cur.execute(query, (username,))
    result = cur.fetchone()

    if result:
        hashed_password = result[0]
        if bcrypt.checkpw(password.encode(), hashed_password.encode()):
            return True
        else:
            return False
    else:
        return False

    conn.close()