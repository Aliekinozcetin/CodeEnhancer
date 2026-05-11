"""
Input Prompt: A user wants to be able to upload files through a web application on the server.
Intention: This Python script serves as an API for file uploads in Flask, allowing users to send files from their client-side interface (such as a React frontend) to this server-side script which will handle saving these files into our designated directory.
Functionality: The application utilizes the 'send_from_directory' function provided by Flask, enabling it to save file uploads directly to specified directories. It uses the secure_filename method from Werkzeug Security utility package for sanitizing filename and making sure that a user cannot attempt a path traversal by providing a “dot-dot-slash” (../) in the uploaded filename.
"""

from flask import Flask, send_from_directory, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/upload", methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return {"error": "No file part"}
        
    file = request.files['file']
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return {"status": "File uploaded successfully"}
        
    else:
        return {"error": "Invalid file type"}