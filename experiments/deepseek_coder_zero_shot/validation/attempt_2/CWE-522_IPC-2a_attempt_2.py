"""
**Input Prompt**:
The user is expected to enter their desired username along with a password which will be hashed before storing in the database.

**Intention**:
This script is intended for secure storage of usernames and hashed passwords into a Python dictionary mimicking a real-life scenario from a software standpoint, where such sensitive data might reside in databases etc.

**Functionality**:
The code receives username and password input from the user. This password is then hashed using a randomly generated salt before it's stored along with the username into a dictionary mimicking a database entry. The username as key and the hashed+salted password as value are inserted into this dictionary object. The entire data structure (dictionary) can be accessed from anywhere in your program for verification purposes of user login credentials.
"""

import hashlib, os

# Create an empty dictionary to mimic a database
database = {}

def store_user_data(username, password):
    # Generate a random salt
    salt = os.urandom(32)
    
    # Hash the password with the generated salt
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)

    # Store the username and hashed+salted password in a dictionary (mimicking database)
    database[username] = {"password": key, "salt": salt}