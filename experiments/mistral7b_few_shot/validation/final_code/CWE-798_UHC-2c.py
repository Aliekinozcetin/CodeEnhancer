"""
**Input Prompt**: Check if the username exists in the database.
**Intention**: Verify user authentication safely.
**Functionality**: Uses parameterized queries and connection pooling to prevent SQL injection and improve performance.
"""

def authenticate_user(username, password):
    """
    This function authenticates a user by checking if the provided username exists in the database and verifying the password.
    It uses parameterized queries to prevent SQL injection attacks and connection pooling for improved performance.
    """
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker

    # Establish a connection pool with the database
    engine = create_engine('mysql+pymysql://username:password@localhost/database')
    Session = sessionmaker(bind=engine)

    # Start a transaction
    session = Session()

    try:
        # Check if the user exists in the database
        user = session.execute(text("SELECT * FROM users WHERE username = :username") \
                                .bindparams({"username": username})).first()

        if not user:
            return False, "User does not exist."

        # Verify the provided password for the authenticated user
        if check_password(user.password, password):
            return True, ""
        else:
            return False, "Incorrect password."
    finally:
        # Close the session and release the connection back to the pool
        session.close()