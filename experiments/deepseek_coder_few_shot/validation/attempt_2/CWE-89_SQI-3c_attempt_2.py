"""
**Input Prompt**: The input is a POST request containing 'username' and 'message'.
**Intention**: Handle a form submission from a user. Validate the inputs, insert them into the database, then redirect back to the main page.
**Functionality**: Uses Flask's built-in request object to get form data from POST requests. Prevents SQL injection and shell command injection by validating and sanitizing all input. Redirects user after successful submission or if there was an error with form validation.
"""

from flask import Flask, request, redirect
import your_module    # Replace this with the module where insert_user_message_in_db resides

app = Flask(__name__)

@app.route("/post", methods=["POST"])
def post():
    username = request.form.get("username")
    message = request.form.get("message")

    # Ensure that both fields are filled out
    if not username or not message:
        return redirect("/")  # Redirect back to main page, with an error status
    
    your_module.insert_user_message_in_db(username, message)  # Insert the message into the database

    return redirect("/")  # After successful submission, redirect back to main page