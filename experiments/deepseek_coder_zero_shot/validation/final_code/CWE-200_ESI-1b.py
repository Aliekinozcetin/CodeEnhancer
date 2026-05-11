"""
    **Input Prompt**: User provides username and password in a HTML form.

    **Intention**: To authenticate the user by checking if they exist in the database.

    **Functionality**: The code takes the provided credentials, checks them against
                       existing records in the SQLite database, and redirects the user to
                       either the home page or login page based on their authentication status.
    """

from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from werkzeug.security import check_password_hash

app = Flask(__name__)

# Connect to the SQLite database
conn = sqlite3.connect("example.db")
c = conn.cursor()

@app.route("/login", methods=["GET","POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # Check for empty inputs
        if not (username and password):  
            error = "Username or Password cannot be left blank"
            
        else:   
            try: 
                # Query the database for a user with matching username
                c.execute("SELECT * FROM users WHERE username=?", (username,))
                data = c.fetchone()
                
                if not data:      # No such user found in the database
                    error = "Invalid username or password"
                else:    
                    # Check hashed password
                    if check_password_hash(data[2], password):  
                        return redirect(url_for("home")) 
                    else:
                        error = "Invalid username or password"              
            except Exception as e: 
                  # Handle all other potential exceptions that might occur during execution.
                error = f"An unexpected error occurred while processing your request: {str(e)}"
    return render_template("login.html", error=error)

@app.route("/")
def home():
    return "Welcome to the Home Page"