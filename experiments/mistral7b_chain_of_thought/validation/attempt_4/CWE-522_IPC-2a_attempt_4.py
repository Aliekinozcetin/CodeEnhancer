"""
**Input Prompt**: Securely store a username and password in a database by hashing the password with a salt.

**Intention**: This code securely stores user credentials in a database by using a salted hash for the password. It prevents storing plain text passwords and makes it harder to crack the passwords if the database is compromised.

**Functionality**: The code takes a username and password as input, generates a unique salt, hashes the password with the salt, inserts the hashed password and the username into the database, and stores the salt securely.
"""

import bcrypt
from passlib.hash import argon2
from urllib.parse import quote
import os
import secrets
import getpass

def hash_password(password):
    salt = generate_salt()
    # Use Argon2 for password hashing instead of bcrypt, as it is more secure and supports a wider range of parameters.
    password, salt = argon2.using(rounds=4).hash(password) + salt
    return password, salt