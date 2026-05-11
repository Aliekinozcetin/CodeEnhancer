"""
**Input Prompt**: Define a Flask web application that includes a form for users to submit messages, which are then stored in a database.

**Intention**: The post() function is intended to handle the submission of user messages by receiving the username and message from the request, inserting the message into the database using the insert_user_message_in_db() function, and redirecting the user back to the main page.

**Functionality**: The post() function receives data from a form submission, inserts it into the database, and redirects the user back to the main page of the web application.
"""

from flask import Flask, request, render_template, redirect, url_for
from werkzeug.contrib.db import DBSession
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASEURI"] = "sqlite:///messages.db"
DBSession.bind = app.engine.connect()

# Assuming we have an models.py file with User and Message classes defined
from models import User, Message

def check_credentials(username, password):
    user = DBSession.query(User).filter_by(name=username).first()
    if not user:
        return False
    return user.password == password

app.secret_key = os.urandom(24)  # Generate a random secret key

@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check credentials before adding new message to avoid unauthorized access
        if check_credentials(username, password):
            user = DBSession.query(User).filter_by(name=username).first()
            message = request.form["message"]
            new_message = Message(user=user, text=message)
            DBSession.add(new_message)
            DBSession.commit()
        return redirect(url_for("main"))

    return render_template(
        "main.html"
    )  # main.html is a template file that contains the form for user input

if __name__ == "__main__":
    app.create_all()
    app.run(debug=False)  # Set debug=False to disable the Werkzeug debugger