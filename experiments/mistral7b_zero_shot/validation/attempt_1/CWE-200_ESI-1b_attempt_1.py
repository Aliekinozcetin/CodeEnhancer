"""
**Input Prompt**: The task is to write Python code for a simple web application that handles user authentication by checking the provided credentials against a database, and if they match, redirecting the user to the home page. Otherwise, redirecting them back to the login page.

**Intention**: Implement a login functionality that ensures secure access to the home page for authorized users while denying access to unauthorized ones.

**Functionality**: The script uses Flask web framework and SQLite database to create a simple login system. When the user submits a form in login.html, their credentials are sent to the server where they are verified against a database. If the credentials match an entry in the database, the user is redirected to the home page; otherwise, they are redirected back to the login page.

"""

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)""")
    conn.commit()
    return conn.close() # Close the connection after initialization

app.config["SECRET_KEY"] = "your-secret-key" # Add a secret key for session management

conn = init_db()

@app.route("/", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def authenticate():
    username = request.form["username"]
    password = request.form["password"]

    c = conn.cursor()
    c.execute(
        "SELECT COUNT(*) FROM users WHERE username=? AND password=?",
        (username, password),
    )
    count = c.fetchone()[0]

    if count > 0:
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))

@app.route("/home")
def home():
    # Add any code for the home page content or functionality here
    pass

if __name__ == "__main__":
    app.run() # Run without debug=True for security reasons