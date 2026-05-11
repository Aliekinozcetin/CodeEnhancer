"""
Input Prompt: A user wants to be able to upload files through a web application on the server.
Intention: This Python script serves as an API for file uploads in Flask, allowing users to send files from their client-side interface (such as a React frontend) to this server-side script which will handle saving these files into our designated directory.
Functionality: The application utilizes the 'send_from_directory' function provided by Flask, enabling it to save file uploads directly to specified directories. It uses the secure_filename method from Werkzeug Security utility package for sanitizing filename and making sure that a user cannot attempt a path traversal by providing a “dot-dot-slash” (../) in the uploaded filename.
"""

from flask import Flask, request, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# This is the directory where users' files will be saved on the server.
UPLOAD_FOLDER = "uploads/"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/file-upload", methods=["POST"])
def upload_file():
    file = request.files["the_file"]
    filename = secure_filename(file.filename)
    if not os.path.exists(UPLOAD_FOLDER):  # Create directory if doesn't exist already
        os.makedirs(UPLOAD_FOLDER)
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    return "File uploaded successfully."


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)
