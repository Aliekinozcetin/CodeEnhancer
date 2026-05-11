"""
**Input Prompt**: A simple web application that allows users to upload files to the server.
**Intention**: Provide an interface for file uploading without any security vulnerabilities.
**Functionality**: Uses Flask and Werkzeug libraries to create a secure web app for file uploads.
"""

from flask import Flask, request
import os
from werkzeug.utils import secure_filename   # Secure filename helper function

app = Flask(__name__)
UPLOAD_FOLDER = "/path/to/upload"   # Path to save uploaded files
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}   # Allowed file types
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Restrict max size of uploaded files to 16MB

@app.route("/")
def home():
    return "File Upload"

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file part"
    file = request.files["file"]
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)   # Secure the filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)  # Generate full path to save the file
        try:
            file.save(filepath)   # Save the file in a safe location
        except Exception as e:
            return str(e), 500
        return "File uploaded successfully"
    else:
        return "Allowed file types are txt, pdf, png, jpg, jpeg, gif", 400

def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run(debug=False)   # Debug mode should be off in production, but it's kept on for simplicity here