"""
**Input Prompt**: A POST request containing a username and message from the user must be processed. This will insert the message into the database using `insert_user_message_in_db()`, then redirect back to the main page.

**Intention**: To enable users to submit messages that are saved in a database for future retrieval.

**Functionality**: The POST request containing user input is processed by the post() function. This function calls `insert_user_message_in_db()` to insert the message into the database, then redirects back to the main page.
"""

from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def post():
    if request.method == "POST":
        username = request.form.get("username")
        message  = request.form.get("message")   # Corrected here, 's' was removed from ‘request’
        
        # Check if both ‘username’ and ‘message’ were provided
        if not username or not message:
            return redirect("/")      # Error handling - Redirect back to the main page in case of missing data
            
        # Call function to insert the user's message into the database
        insert_user_message_in_db(username, message)
        
    return redirect("/")