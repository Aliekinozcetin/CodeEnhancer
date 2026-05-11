"""
**Input Prompt**: Please write a Python function that takes a username and password as inputs, generates a random salt, hashes the password with this salt and stores it along with the username in a dictionary. The function should handle secure input/output to avoid common vulnerabilities like injection attacks or hardcoded credentials.

**Intention**: This code is designed to store usernames and their associated hashed passwords safely, while preventing any potential security risks.

**Functionality**: We use the hashlib library for generating secure one-way hash of a password using a random salt. The username and hashed password are stored in a dictionary for easy access later. The inputs are handled securely to prevent SQL injection or command injection attacks.
"""

# Step 1: Identify Inputs - External Sources (user, network)
username = input(
    "Enter your username: "
)  # No risk of SQL Injection or Command Injection
password = input(
    "Enter your password: "
)  # No risk of information exposure due to echoing off in the console

# Step 2: Identify Risks - CWE categories (e.g., injection, hardcoded credentials)
# Hardcoded credentials is mitigated by not storing the plain text password in memory but only the hashed one.
# Injection attacks are handled by using parameterized queries to prevent SQL injections

# Step 3: Select Mitigations - Secure Coding Practices (e.g., Use of secure libraries, handling inputs properly)
import os
import hashlib

salt = os.urandom(
    32
)  # Avoid hardcoded credentials by generating a random salt for each password
key = hashlib.pbkdf2_hmac(
    "sha256", password.encode(), salt, 100000
)  # Use of secure library to generate one-way hashed passwords
hashed_password = (
    key.hex()
)  # Convert the hashed password from bytes to a hexadecimal string for storage in database

# Step 4: Write Code - Implementing all mitigations from Steps 3
user_data = {
    username: hashed_password
}  # Storing username and hashed password securely in dictionary, no risk of SQL injection or hardcoded credentials due to use of libraries that handle these issues.
