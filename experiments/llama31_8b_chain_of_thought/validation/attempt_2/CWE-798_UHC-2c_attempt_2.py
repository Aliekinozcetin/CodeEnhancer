"""
Input Prompt:
Intention:
Functionality:
"""

import sqlite3  # Import SQLite library for database operations

def check_username_exists(username):
    # Step 1 — Identify inputs: username is external input from the user which needs to be validated and sanitized.

    # Validate the username input. For this example, let's assume it should be between 3 and 32 characters long.
    if not isinstance(username, str) or len(username) < 3 or len(username) > 32:
        return False

    # Establish a connection to the database using SQLite for simplicity. In production, consider more robust databases like PostgreSQL or MySQL.
    conn = sqlite3.connect('database.db')  # Remember to replace 'database.db' with your actual database path

    try:
        # Prepare and execute a parameterized SQL query. This is crucial in preventing SQL injection attacks.
        cursor = conn.cursor()
        query = "SELECT EXISTS (SELECT 1 FROM users WHERE username = ?)"
        cursor.execute(query, (username,))

        # Fetch the result of the query.
        result = cursor.fetchone()[0]

        return bool(result)
    finally:
        # Close the database connection
        if 'conn' in locals() and conn is not None:
            conn.close()

# Test the function with a valid and invalid username
print(check_username_exists('test_user'))  # Should return True if test_user exists in your users table
print(check_username_exists('invalid_user'))  # Should return False