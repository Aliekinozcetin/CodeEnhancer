"""
**Input Prompt**: Connect to a SQLite database and check if a provided username exists in the database. If the username exists it returns true otherwise it returns false.

**Intention**: This code is designed to verify user authentication by checking if a given username exists within the database.

**Functionality**: The program opens a connection to an SQLite database, executes a query to check for the existence of a provided username, and then closes the connection. If the username does exist, it returns True; otherwise, it returns False.
"""

import sqlite3

def is_username_exists(username):
    # Connect to SQLite database
    conn = None
    try:
        conn = sqlite3.connect("my_database.db")
        cursor = conn.cursor()

        # Query the username from 'users' table
        cursor.execute("SELECT 1 FROM users WHERE username=?", (username,))
        
        result = cursor.fetchone()
    except Exception as e:
        if conn is not None:
            conn.close()
        raise e
    
    if result is not None:     # If result contains something 
        return True           # a row was found so return True
    else:                     # Close the connection only when username doesn't exist. Not in finally clause to be more pythonic and prevent ResourceWarning on exit.
        if conn is not None:
            conn.close()