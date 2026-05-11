"""
    **Input Prompt**: A POST request to /login with username & password as form data.

    **Intention**: To authenticate a user trying to log into the system.

    **Functionality**: Validates username/password, redirects appropriately based on authentication result.
    """

from flask import request, redirect, url_for
from werkzeug.security import (
    check_password_hash,
)   # Assumes you have Werkzeug installed  (pip install werkzeug) for password hashing and comparison
import sqlite3   # Assumes SQLite database is in use
import flask_sqlalchemy

app = Flask(__name__)
db = flask_sqlalchemy.SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    
@app.route("/login", methods=["POST"])
def login():
    # Step 1: Identify Inputs
    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password, password):
        return redirect(url_for("login"))  # Redirect to login page if invalid credentials
        
    # If credentials are valid, proceed to homepage. This would typically be done by starting a session and setting session variables.
    # For simplicity, we'll just redirect here:
    return redirect(url_for("home"))