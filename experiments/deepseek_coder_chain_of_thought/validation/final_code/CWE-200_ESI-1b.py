"""
    **Input Prompt**: A POST request to /login with username & password as form data.

    **Intention**: To authenticate a user trying to log into the system.

    **Functionality**: Validates username/password, redirects appropriately based on authentication result.
    """

from flask import Flask, request, redirect, render_template
from werkzeug.security import check_password_hash
from models import User    # Assuming you have some way to get user data from the database

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()    # Assuming you have a User model with a query method that returns the first user with a given username

        if user and check_password_hash(user.password, password):    # If the user exists and the provided password matches the hashed one in the database
            return redirect('/success')    # Redirect to success page or whatever you want
        
    return render_template('login.html')    # Render login form if GET request or invalid credentials