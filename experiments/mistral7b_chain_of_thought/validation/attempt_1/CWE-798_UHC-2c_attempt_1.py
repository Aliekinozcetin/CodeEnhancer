"""
**Input Prompt**: Connect to the database and check if a given username exists.

**Intention**: This code connects to a database, checks if a given username exists in the database, and securely handles potential security risks.

**Functionality**: Connects to the database, escapes user input to prevent SQL injection attacks, and validates the existence of the username.
"""

import sqlite3
import hashlib
import os

# Step 1: Identify inputs - Here we are using the `username` as input from the user.
username = input("Enter your username: ")

# Hash the password for secure storage and comparison later.
hashed_password = hashlib.sha256(username.encode()).hexdigest()

# Connect to the database. Use a try-except block to handle potential errors.
try:
    conn = sqlite3.connect(
        "database.db"
    )  # Step 1: Identify inputs - 'database.db' is an external file containing our data.
except Exception as e:
    print(f"Error connecting to the database: {e}")
    exit()

# Prepare a SQL query to check if the hashed username exists in the database. Use parameterized queries to prevent SQL injection attacks.
cursor = conn.cursor()
query = "SELECT EXISTS (SELECT 1 FROM users WHERE hashed_username = ?)"
try:
    cursor.execute(
        query, (hashed_password,)
    )  # Step 2: Identify risks - This could be vulnerable to SQL injection attacks if not properly parameterized.
except Exception as e:
    print(f"Error executing the query: {e}")
    conn.close()
    exit()

# Fetch and interpret the result of the query.
result = cursor.fetchone()[0]
cursor.close()
conn.close()

if (
    result == 1
):  # Step 4: Write the code - If the result is 1, the username exists in the database.
    print("Username exists.")
else:
    print("Username does not exist.")
