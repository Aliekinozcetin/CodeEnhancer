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

def post():
    username = request.form['username']
    message = request.form['message']

    if re.search(r'['';"\n]', username) or re.search(r'['';"\n]', message):
        return "Invalid input detected. Please try again."

    hashed_username = hashlib.sha256(username.encode()).hexdigest()

    response = requests.post('http://localhost:5001/insert', json={'hashed_username': hashed_username, 'message': message})

    if response.ok:
        return redirect(url_for('main'))
    else:
        return "Error occurred while inserting message into the database."

class MessageForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    message = StringField('Message', validators=[DataRequired(), Length(min=1, max=255)])
    submit = SubmitField('Send Message')