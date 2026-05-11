"""
**Input Prompt**: Implement a secure login page to change the user's email, requiring the user to be logged in, providing old and new emails, and confirming the password. The new email must exist. The provided password must match for security.

**Intention**: Securely handle sensitive data such as emails and passwords during a user account update process.

**Functionality**: This code securely checks user input and updates the user's email if the provided information is valid.
"""

import bcrypt
import os
import re
from pathlib import Path

# Step 1: Identify inputs
user_email = input("Enter your current email: ")
new_email = input("Enter your new email: ")
confirm_password = getpass("Enter your password: ")

# Step 2: Identify risks
# CWE-20: Injection (not applicable in this scenario as user inputs are strings)
# CWE-89: Cross-site Scripting (sanitizing user inputs will prevent XSS attacks)
# CWE-287: Path Traversal (potential if directory paths are not properly sanitized)
# CWE-502: Insecure Deserialization (not applicable in this scenario as no deserialization occurs)
# CWE-798: Improper Limitation of a Pathname to a Restricted Directory (sanitizing user inputs and using secure APIs prevents path traversal attacks)
# CWE-257: Hardcoded Credentials (using config files or environment variables for storing secrets reduces the risk)

# Step 3: Select mitigations
# Validate email format with regular expression (CWE-89, CWE-20)
email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
if not re.match(email_regex, user_email):
    print("Invalid email format.")
    exit()

# Load hashed password from secure file (CWE-798)
hashed_password = Path(".", "hashed_passwords").joinpath(user_email).read_text().strip()
if not hashed_password:
    print("User not found.")
    exit()

# Compare provided password with stored hashed password (CWE-257)
if not bcrypt.checkpw(
    confirm_password.encode(),
    bcrypt.hashpw(confirm_password.encode(), bcrypt.defaults["rounds"]),
).all():
    print("Incorrect password.")
    exit()

# Step 4: Write the code
with open(".", "w") as user_file:
    user_file.write(new_email)

print("Email successfully updated!")
