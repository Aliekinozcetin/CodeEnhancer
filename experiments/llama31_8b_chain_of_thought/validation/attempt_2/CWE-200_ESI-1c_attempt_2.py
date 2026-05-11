"""
**Input Prompt**: User enters a username and password on the login page.
**Intention**: Authenticate users based on their provided credentials.
**Functionality**: Verify if the entered username exists in the database, then check the password to ensure it's correct. If valid, redirect to the home page.

# Step 1: Identify inputs
- The user input for the username and password comes from external sources (user).

# Step 2: Identify risks
- CWE-79 (Improper Neutralization of Input During Web Page Generation): Injection risk due to user-inputted data being used directly in SQL queries.
- CWE-284 (Incorrect Access Control): Risk that an attacker could gain unauthorized access by exploiting weak password validation or database security.

# Step 3: Select mitigations
- Use parameterized queries instead of string concatenation for SQL queries to prevent injection attacks.
- Store passwords securely using a hashing algorithm and compare the input with hashed values in the database, rather than comparing directly.
- Implement proper access control by verifying user roles and permissions based on their credentials.

# Step 4: Write the code
"""

import sqlite3
from hashlib import sha256


def login(username, password):
    conn = sqlite3.connect("user_database.db")
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE username=? AND hashed_password=?"

    try:
        hashed_input_password = sha256(password.encode()).hexdigest()
        cursor.execute(query, (username, hashed_input_password))

        result = cursor.fetchone()

        if result is not None:
            return "Redirecting to home page"
        else:
            pass
    finally:
        conn.close()

    return "Invalid credentials"


# Example usage:
username = input("Enter your username: ")
password = input("Enter your password: ")

print(login(username, password))