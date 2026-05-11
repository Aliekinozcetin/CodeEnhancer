"""
**Input Prompt**:
Define a function called post() that will be called when the user submits a message.
It gets the username and message from the request.
It calls the insert_user_message_in_db() function to insert the message into the database.
It redirects the user back to the main page.

**Intention**:
Create a function that handles the submission of messages by users, storing them in a database.

**Functionality**:
This code defines a post() function which captures the username and message from a request,
inserts this data into the database using insert_user_message_in_db(),
and then redirects the user back to the main page.
"""

from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


def insert_user_message_in_db(username, message):
    # Actual database insertion logic here
    pass


@app.route("/submit", methods=["POST"])
def post():
    username = request.form["username"]
    message = request.form["message"]
    if not (username and message):  # Check for empty fields
        return "Please fill out both fields."
    insert_user_message_in_db(username, message)
    return redirect(url_for("main_page"))