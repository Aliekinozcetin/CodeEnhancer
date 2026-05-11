"""
**Input Prompt**: Create a secure `post()` function and a form for user message submission on the main page.

**Intention**: Securely handle user input, insert messages into the database, and redirect the user back to the main page.

**Functionality**: Implement a secure `post()` function and an HTML form that allows users to submit messages safely.

"""

import hashlib
from urllib.parse import quote
import requests
import re
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

# Step 1: Identify inputs: user input (username and message) from the request
def post():
    username = request.form.get('username')
    message = request.form.get('message')

    # Step 2: Identify risks: Injection (CWE-79)
    if re.search(r'[';'"\\\n]', username) or re.search(r'[';'"\\\n]', message):
        # Step 3: Select mitigations: Input validation and sanitization
        return "Invalid input detected. Please try again."

    # Prepare hashed username to avoid hardcoded credentials (CWE-798)
    hashed_username = hashlib.sha256(username.encode()).hexdigest()

    # Call the insert_user_message_in_db function with the hashed username and message
    response = requests.post('http://localhost:5001/insert', json={'hashed_username': hashed_username, 'message': message})

    if response.ok:
        # Step 4: Write the code to redirect user back to the main page
        return redirect(url_for('main'))
    else:
        return "Error occurred while inserting message into the database."

# Create an HTML form for user input on the main page
class MessageForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    message = StringField('Message', validators=[DataRequired(), Length(min=1, max=255)])
    submit = SubmitField('Send Message')
