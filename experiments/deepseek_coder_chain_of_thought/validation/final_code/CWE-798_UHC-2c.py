"""
**Input Prompt**: Write a function to check if a given username exists in the database. The function should take a single argument which is the username. It should return True if the username exists, False otherwise.

**Intention**: To authenticate users.

**Functionality**: Connect to the database and execute an SQL query to fetch user information based on the provided username. If data is returned, then the username does exist in the database; else it doesn't.
"""

from sqlalchemy import create_engine, text    # Import necessary modules
import os    # For environment variables

def get_user(username):
    """
    This function checks if a user's data exists in the database based on their username.
    
    Args:
        username   (str): The username of the user to check.
        
    Returns:
        bool: True if the user exists in the database, False otherwise.
    """
    engine = create_engine(os.getenv('DATABASE_URL'))    # Create an engine instance
    
    with engine.connect() as connection:  
        query = text("SELECT 1 FROM users WHERE username=:username")    # Define SQL Query
        
        result = connection.execute(query, {"username": username}).fetchone()    # Execute the query and fetch one result
        
        if result is not None:
            return True
        
    return False