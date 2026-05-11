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
    """
    Inserts a user message into the database.

    Args:
        username (str): The username of the user who submitted the message.
        message (str): The content of the user's message.
    """
    # Actual database insertion logic here
    pass


@app.route("/submit", methods=["POST"])
def post():
    """
    Handles the submission of a user message.

    Returns:
        redirect: Redirects to the main page after submitting a message.
    """
    if request.method == "POST":
        username = request.form["username"]
        message = request.form["message"]
        insert_user_message_in_db(username, message)
    return redirect(url_for("main_page"))


@app.route("/")
def main_page():
    """
    Renders the main HTML template.

    Returns:
        render_template: The main.html template.
    """
    return render_template("main.html")


if __name__ == "__main__":
    app.run(debug=False)  # Disable debug mode