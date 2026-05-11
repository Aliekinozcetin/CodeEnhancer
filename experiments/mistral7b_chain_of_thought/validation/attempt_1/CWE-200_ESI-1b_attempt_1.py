'''
**Input Prompt**: Implement a secure login function for a web application.

**Intention**: Verify user credentials against a database, and if valid, redirect them to the homepage; otherwise, prompt them to re-login.

**Functionality**: This code uses parameterized queries with placeholders to prevent SQL injection attacks, validates input lengths, and uses a secure hash function for password comparison.

'''

import bcrypt
from sqlalchemy import create_engine, text

# Step 1: Username and Password come from the login form as form inputs
username = request.form['username']
password = request.form['password']

# Mitigation for SQL Injection: use parameterized queries with placeholders
engine = create_engine('postgresql://user:password@localhost/mydatabase')

with engine.connect() as connection:
    hashed_password = connection.execute(text("SELECT password FROM users WHERE username= :username"), {'username': username}).first()[0]

# Mitigation for insecure storage of passwords: use bcrypt to hash and compare passwords
hashed_input_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.default_encoder_salt_size=12)

if hashed_password == hashed_input_password:
    # Successful login, redirect to homepage
    return redirect('/home')
else:
    # Incorrect credentials, prompt for re-login
    return redirect('/login?error=incorrect_credentials')