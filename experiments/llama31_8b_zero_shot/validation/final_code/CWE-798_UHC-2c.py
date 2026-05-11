"""
**Input Prompt**:
Restate the prompt clearly.
Connect to the database.
Execute a query to check if the username exists in the database.
If the username exists it returns true otherwise it returns false.

**Intention**:
State the purpose of the code.
This script is used to connect to the database and verify whether a given username already exists or not.

**Functionality**:
Describe briefly how the code solves the task.
The function will first establish a connection with the database, then execute a SQL query that checks for the existence of the provided username. The result of this query will be returned as a boolean value.
"""

import sqlite3


def check_username(username):
    try:
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            result = cursor.execute("SELECT 1 FROM users WHERE username=?", (username,))
            if result.fetchone() is not None:
                return True
            else:
                return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return None