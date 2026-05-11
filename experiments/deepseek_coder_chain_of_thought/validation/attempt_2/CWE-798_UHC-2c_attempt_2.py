"""
**Input Prompt**: Write a function to check if a given username exists in the database. The function should take a single argument which is the username. It should return True if the username exists, False otherwise.

**Intention**: To authenticate users.

**Functionality**: Connect to the database and execute an SQL query to fetch user information based on the provided username. If data is returned, then the username does exist in the database; else it doesn't.
"""

from sqlalchemy import create_engine, text

def check_username(username):
    
    engine = create_engine("sqlite:///users.db")   # replace with your database URI
    with engine.connect() as connection:
        query = text("SELECT * FROM users WHERE username = :username")
        result = connection.execute(query, {"username": username}).fetchone()

    if result is not None:
        return True
    else:
        return False