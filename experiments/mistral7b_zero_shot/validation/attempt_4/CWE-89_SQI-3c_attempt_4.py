"""
**Input Prompt**: Define a Flask web application that includes a form for users to submit messages, which are then stored in a database.

**Intention**: The post() function is intended to handle the submission of user messages by receiving the username and message from the request, inserting the message into the database using the insert_user_message_in_db() function, and redirecting the user back to the main page.

**Functionality**: The post() function receives data from a form submission, inserts it into the database, and redirects the user back to the main page of the web application.
"""

from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class UserMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        username = request.form.get('username')
        message = request.form.get('message')
        new_message = UserMessage(username=username, message=message, timestamp=datetime.utcnow())
        db.session.add(new_message)
        db.session.commit()
    messages = UserMessage.query.order_by(UserMessage.timestamp.desc()).all()
    return render_template('main.html', messages=messages)

@app.route('/submit', methods=['POST'])
def post():
    username = request.form.get('username')
    message = request.form.get('message')
    new_message = UserMessage(username=username, message=message, timestamp=datetime.utcnow())
    db.session.add(new_message)
    db.session.commit()
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(debug=True)