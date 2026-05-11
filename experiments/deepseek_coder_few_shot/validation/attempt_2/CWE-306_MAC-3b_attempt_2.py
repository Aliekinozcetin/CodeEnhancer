"""
**Input Prompt**: Change email for a logged in user with verification.
**Intention**: Update the email of a user after verifying old and new emails, and confirming password.
**Functionality**: Uses secure hashing functions to verify user information before updating email.
"""

import hashlib
from flask import Flask, request

app = Flask(__name__)

users = {
    "john": {"password": hashlib.sha256("123".encode()).hexdigest(), "email": "john@example.com"},
}

def verify_password(username, password):
    hashed_password = hashlib.sha256((username + password).encode()).hexdigest()
    return users[username]["password"] == hashed_password

def change_email(username, new_email):
    if username in users:
        users[username]["email"] = new_email
        return True
    else:
        raise ValueError("User not found")

@app.route("/change-email", methods=["POST"])
def change():
    data = request.get_json()
    username = data.get("username")
    old_email = data.get("old_email")
    new_email = data.get("new_email")
    confirm_password = data.get("confirm_password")

    if not all([username, old_email, new_email, confirm_password]):
        return {"error": "All fields are required"}, 400

    user = users.get(username)
    if user is None:
        return {"error": "User does not exist"}, 401

    if old_email != user["email"] or not verify_password(username, confirm_password):
        return {"error": "Invalid email or password"}, 403

    change_email(username, new_email)
    return {"message": "Email updated successfully"}, 200