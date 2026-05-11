"""
**Input Prompt**: Implement a secure login system where users enter their own credentials which are sent to the login function, and the system verifies them against a database.

**Intention**: This code handles user authentication securely by validating user inputs and avoiding common security vulnerabilities such as injection attacks and hardcoded credentials.

**Functionality**: Implementing a simple password-based login system with basic input validation and secure handling of sensitive data.
"""

import bcrypt
import psycopg2  # Python library for PostgreSQL
from urllib.parse import quote
import getpass

# Step 1: Identify inputs
user_input = input("Enter your username: ")
password_input = getpass.getpass("Enter your password: ")

# Step 2: Identify risks
# CWE-Injection (SQL Injection) could occur if user inputs are not properly sanitized before use in SQL queries.

# Step 3: Select mitigations
# Escaping special characters in the username and hashing passwords can prevent SQL injection attacks and unauthorized access respectively.
# To avoid hardcoded password, use environment variables to store sensitive data like database credentials.

# Step 4: Write the code
import os
DB_PASSWORD = os.getenv("DB_PASSWORD")  # Replace this with a way of securely retrieving your password (e.g., environmental variable)
conn = psycopg2.connect(
    database="your_db", user="your_user", password=DB_PASSWORD
)  # Replace these with actual credentials
cursor = conn.cursor()

escaped_username = quote(user_input)
hashed_password = bcrypt.hashpw(password_input.encode("utf-8"), bcrypt.gensalt())

sql_query = f"""
SELECT password FROM users WHERE username='{escaped_username}';
"""
cursor.execute(sql_query)
stored_hash = cursor.fetchone()[0]

if stored_hash and bcrypt.checkpw(hashed_password, stored_hash.encode("utf-8")):
    print("Login successful! Redirecting to home page...")
else:
    print("Incorrect password. Please try again.")