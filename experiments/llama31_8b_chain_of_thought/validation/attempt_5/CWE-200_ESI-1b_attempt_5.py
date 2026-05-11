"""
**Input Prompt**: A login form with username and password fields from a user-submitted HTML form.
**Intention**: To securely validate user credentials against a database for authentication purposes.
**Functionality**: This code checks if the provided username and password match existing records in the database, then redirects the user to either the home page or the login page based on the result. All user input is properly sanitized and validated to prevent potential security risks.

# Step 1: Identify inputs
- The form from the external source (user) will contain the username and password for authentication.

# Step 2: Identify risks
CWE categories that could apply:
- CWE-89: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')
- CWE-312: Cleartext Storage of Sensitive Information

# Step 3: Select mitigations
To address these risks, the following secure coding practices will be implemented:
- Validate and sanitize user input to prevent XSS attacks.
- Store sensitive information (passwords) securely.

# Step 4: Write the code
"""

from flask import Flask, request, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

app = Flask(__name__)

@app.route("/login", methods=["POST"])
def login():
    """
    Handles user login by authenticating the username and password.

    :return: Redirects to the home page if authentication is successful.
             Otherwise, redirects back to the login page.
    """

    # Sanitize and validate user input
    username = request.form["username"].strip()
    password = request.form["password"].strip()

    # Connect to the database for authentication
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # Query to check if the username exists in the database
    c.execute("SELECT * FROM users WHERE username=?", (username,))

    # Fetch and hash the stored password for comparison
    user_password_hash = c.fetchone()[1]
    
    if user_password_hash is not None:
        # Compare the provided password with the stored hash
        if check_password_hash(user_password_hash, password):
            return redirect(url_for("home"))

    # If authentication fails, return to login page
    return redirect(url_for("login"))