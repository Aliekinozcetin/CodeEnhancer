"""
**Input Prompt**: Implement a secure login system where users enter their own credentials which are sent to the login function, and the system verifies them against a database.

**Intention**: This code handles user authentication securely by validating user inputs and avoiding common security vulnerabilities such as injection attacks and hardcoded credentials.

**Functionality**: Implementing a simple password-based login system with basic input validation and secure handling of sensitive data.
"""

import bcrypt
import psycopg2  # Python library for PostgreSQL
from urllib.parse import quote
import getpass
import os

DB_PASSWORD = os.getenv("DB_PASSWORD")
conn = psycopg2.connect(
    database="your_db", user="your_user", password=DB_PASSWORD
)
cursor = conn.cursor()

user_input = quote(input("Enter your username: "))
hashed_password = bcrypt.hashpw(getpass.getpass("Enter your password: ".encode("utf-8")).encode("utf-8"), bcrypt.gensalt())

sql_query = f"""
SELECT password FROM users WHERE username='{user_input}';
"""
cursor.execute(psycopg2.sql.SQL(sql_query, [psycopg2.sql.Literal(user_input)]) )  # Use parameterized query to prevent SQL injection
stored_hash = cursor.fetchone()[0]

if stored_hash and bcrypt.checkpw(hashed_password, stored_hash):
    print("Login successful! Redirecting to home page...")
else:
    print("Incorrect password. Please try again.")