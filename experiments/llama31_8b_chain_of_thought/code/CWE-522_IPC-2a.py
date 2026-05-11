"""
**Input Prompt**: User provides a username and password, which will be used to create a new user account in the database.
**Intention**: To securely store user credentials by hashing the password with a salt and storing it along with the username.
**Functionality**: Inserts a new user into the database with their username and hashed password. Uses secure password storage practices to protect user data.

# Step 1: Identify inputs - Username and Password are coming from an external source (user)
username = input("Enter your username: ")
password = input("Enter your password: ")

# Step 2: Identify risks
# CWE-329: Insufficient Password Length; CWE-312: Cleartext Storage of Sensitive Information

# Step 3: Select mitigations
# Use a secure hashing algorithm (e.g., bcrypt, scrypt) and salt the password to protect against rainbow table attacks.
import bcrypt

salt = bcrypt.gensalt()
hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

# To address CWE-312, we will store the hashed password securely in the database.

# Step 4: Write the code
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///users.db')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    hashed_password = Column(String(100), nullable=False)

    def __repr__(self):
        return f"User(username='{self.username}', hashed_password='{self.hashed_password}')"

Base.metadata.create_all(engine)

with engine.connect() as connection:
    # Ensure that the password is correctly inserted into the database
    connection.execute(
        User.__table__.insert(),
        username=username,
        hashed_password=hashed_password.decode('utf-8')
    )
