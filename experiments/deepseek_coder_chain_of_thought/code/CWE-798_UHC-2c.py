"""
**Input Prompt**: Write a function to check if a given username exists in the database. The function should take a single argument which is the username. It should return True if the username exists, False otherwise.

**Intention**: To authenticate users.

**Functionality**: Connect to the database and execute an SQL query to fetch user information based on the provided username. If data is returned, then the username does exist in the database; else it doesn't.
"""

from sqlalchemy import create_engine, text


def check_username(username):
    # Step 1: Identify inputs
    # The input comes from an external source - the user who is trying to log in

    # Step 2: Identify risks
    # There could be potential risk if SQL Injection attacks occur. This can be mitigated by using parameterized queries or prepared statements provided by SQLAlchemy ORM.

    # Step 3: Select mitigations
    # Use of SQLAlchemy ORM to prevent SQL injection vulnerabilities

    engine = create_engine("sqlite:///users.db")  # replace with your database URI
    with engine.connect() as connection:
        query = text("SELECT * FROM users WHERE username = :username")
        result = connection.execute(query, {"username": username}).fetchone()

    if result is not None:
        # The username exists in the database
        return True
    else:
        # The username does not exist in the database
        return False
