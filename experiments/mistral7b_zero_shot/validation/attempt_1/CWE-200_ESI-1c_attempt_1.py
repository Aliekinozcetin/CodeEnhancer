"""
**Input Prompt**: User enters a username and password in the login page, which are sent to the login function.

**Intention**: The code aims to verify the entered username and password with the records stored in the database, and if they match, redirect the user to the home page.

**Functionality**: It uses a hypothetical Database object for querying user credentials from the database. If the entered username exists and the password matches, it redirects the user to the home page using `redirect` function (assuming Flask is being used).

Note: This code assumes that you have the necessary Database interaction setup. In this example, I've used a mock database for simplicity.
"""

from flask import Flask, render_template, redirect, request, url_for
import mock_database

app = Flask(__name__)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if mock_database.user_exists(username):
            if mock_database.check_password(username, password):
                return redirect(url_for("home"))

    return render_template("login.html")


@app.route("/")
def home():
    return "Welcome to the Home Page!"


if __name__ == "__main__":
    app.run()
