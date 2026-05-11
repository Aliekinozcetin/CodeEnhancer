"""
**Input Prompt**: Accepting username and password from login page, checking them against database records, and redirecting or not based on results.
**Intention**: Authenticate users by checking their credentials safely with a database query.
**Functionality**: Uses SQLite3 to securely compare provided credentials with those stored in the database.
"""

import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    if verify_user(username, password):
        return redirect(url_for("home"))
    else:
        return "Invalid credentials"

def verify_user(username: str, password: str) -> bool:
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    rows = cursor.execute("SELECT  * FROM users WHERE username  = ?", (username,)).fetchall()
    
    if len(rows) == 0:
        return False
        
    hashed_password = generate_password_hash(rows[0][2])   # Assuming password hash is in the third column of database

    conn.close()

    # Checking provided password against stored one (after fetching from database)
    return check_password_hash(hashed_password, password)