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
        return "Invalid credentials", 401