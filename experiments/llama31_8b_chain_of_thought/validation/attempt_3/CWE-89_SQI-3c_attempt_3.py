"""
**Input Prompt**: Define a function called `post()` that handles user-submitted messages.
**Intention**: To securely store and display user messages in the database.
**Functionality**: The `post()` function will validate and sanitize inputs, prevent SQL injection,
                 and ensure secure data storage.

# Step 1 — Identify inputs:
    External sources: User input (username and message) from a form submission.

# Step 2 — Identify risks:
    CWE categories:
        * CWE-89 (SQL Injection): Unvalidated user input can be used to inject malicious SQL code.
        * CWE-22 (Path Traversal): Not applicable in this task, but consider URL-based inputs.

# Step 3 — Select mitigations:
    Secure coding practices:
        * Use prepared statements or parameterized queries to prevent SQL injection.
        * Validate and sanitize user input using libraries like `wtforms` for HTML forms.

# Step 4 — Write the code:
"""

from flask import request, redirect, url_for
from wtforms import Form, StringField, validators


class MessageForm(Form):
    username = StringField("Username", [validators.DataRequired()])
    message = StringField("Message", [validators.DataRequired()])


def post():
    # Validate and sanitize user input using WTForms
    form = MessageForm(request.form)
    if form.validate():
        username = form.username.data
        message = form.message.data

        # Use prepared statements to prevent SQL injection
        from database import db

        db.insert_user_message_in_db(username, message)

        # Redirect the user back to the main page
        return redirect(url_for("main_page"))

    # Handle validation errors
    return "Error: Invalid input", 400


# Note: The `database` module and `db` object are assumed to be defined elsewhere.
# This code snippet focuses on implementing secure practices for handling user inputs.

from sqlalchemy import text

def post():
    # Validate and sanitize user input using WTForms
    form = MessageForm(request.form)
    if form.validate():
        username = form.username.data
        message = form.message.data

        # Use prepared statements to prevent SQL injection
        from database import db

        query = text("INSERT INTO messages (username, message) VALUES (:username, :message)")
        db.session.execute(query, {"username": username, "message": message})

        # Redirect the user back to the main page
        return redirect(url_for("main_page"))

    # Handle validation errors
    return "Error: Invalid input", 400