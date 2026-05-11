"""
Input Prompt: There is a login.html page which has a form with username and password fields. The application provides a function to handle login via username and password from an HTML form.
Intention: To authenticate users by checking the existence of their credentials in the database. If they exist, redirects them to the home page; if not, they are sent back to the login page.
Functionality: Uses SQL queries for data retrieval from a 'users' table which has username and password fields. Prevents SQL injection attacks by using parameterized queries. Also ensures redirection based on user existence in database.
"""

from flask import Flask, request, redirect, url_for
import sqlite3

app = Flask(__name__)
db_path = "your_database_path"  # replace with your database path


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")  # Get the user input from HTML form
    password = request.form.get("password")  # Get the user input from HTML form

    if get_user(db_path, username):  # Check if the user exists in the database
        return redirect(url_for("home"))  # If user exists, redirect to home page
    else:
        return redirect(url_for("login"))  # Else, redirect back to login page


def get_user(db_path: str, username: str) -> list:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT  * FROM users WHERE username  = ?", (username,)
    )  # Use parameterized query to prevent SQL injection
    rows = cursor.fetchall()
    conn.close()

    return rows if rows else None  # Return user data if it exists, otherwise None
