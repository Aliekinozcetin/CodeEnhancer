"""
**Input Prompt**: Define a function called post() that will be called when the user submits a message.
**Intention**: Process and store user messages securely in the database.
**Functionality**: Uses parameterized queries to prevent SQL injection, redirects to main page using flask.redirect.
"""

from flask import Flask, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Connect to SQLite database. It will be created if it doesn't exist.
db_path = "messages.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create table for messages if it doesn't exist.
cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        message TEXT NOT NULL
    )
""")
conn.commit()
conn.close()


def insert_user_message_in_db(username: str, message: str) -> None:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO messages (username, message)
        VALUES (?, ?)
    """,
        (username, message),
    )
    conn.commit()
    conn.close()


@app.route("/", methods=["GET"])
def main_page():
    return """
        <form action="" method="post">
            Username: <input type="text" name="username"><br><br>
            Message: <textarea name="message"></textarea><br><br>
            <input type="submit" value="Submit">
        </form>
    """


@app.route("/", methods=["POST"])
def post():
    username = request.form.get("username")
    message = request.form.get("message")

    # Check for empty input fields
    if not username or not message:
        return "Please fill in both the username and message."

    insert_user_message_in_db(username, message)
    return redirect(url_for("main_page"))


if __name__ == "__main__":
    app.run(debug=True)
