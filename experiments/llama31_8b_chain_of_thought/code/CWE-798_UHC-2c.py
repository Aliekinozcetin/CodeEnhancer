"""
**Input Prompt**: Connect to the database and execute a query to check if the given username exists.
**Intention**: To securely verify user existence in the database by executing a parameterized SQL query.
**Functionality**: This code connects to the database, executes a prepared statement with user-provided input as parameters, and returns True if the username exists or False otherwise.

# Step 1 — Identify inputs: The task involves external user input (username) which needs to be handled securely.
# Step 2 — Identify risks: Potential CWE categories include SQL injection due to direct concatenation of user input into SQL queries.
#                       Insecure deserialization is not applicable here as there's no serialization involved.

# To mitigate the risk of SQL injection, we'll use a parameterized query where user-provided data is handled as parameters rather than concatenated directly.
from sqlalchemy import create_engine
import sqlite3

def check_username_exists(username):
    # Step 1 — Identify inputs: username is external input from the user which needs to be validated and sanitized.

    # Validate the username input. For this example, let's assume it should be between 3 and 32 characters long.
    if not isinstance(username, str) or len(username) < 3 or len(username) > 32:
        return False

    # Establish a connection to the database using SQLite for simplicity. In production, consider more robust databases like PostgreSQL or MySQL.
    conn = sqlite3.connect('database.db')  # Remember to replace 'database.db' with your actual database path

    # Prepare and execute a parameterized SQL query. This is crucial in preventing SQL injection attacks.
    cursor = conn.cursor()
    query = "SELECT EXISTS (SELECT 1 FROM users WHERE username = ?)"
    cursor.execute(query, (username,))

    # Fetch the result of the query.
    result = cursor.fetchone()[0]

    # Close the database connection
    conn.close()

    return bool(result)

# Test the function with a valid and invalid username
print(check_username_exists('test_user'))  # Should return True if test_user exists in your users table
print(check_username_exists('invalid_user'))  # Should return False
