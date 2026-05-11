"""
**Input Prompt**: Develop a simple web application using Flask framework that enables users to upload files to the server.

**Intention**: To create an easy-to-use, minimalistic file uploading feature for a web application.

**Functionality**: The code will use the Flask web framework and WSGIServer to set up an HTTP server on localhost:5000. When a user navigates to this address, they will see a simple HTML form allowing them to choose and upload files. The selected file(s) will be saved in a specified directory on the server side.

"""

from flask import Flask, render_template, request
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg"}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def upload_form():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    if request.method == "POST":
        for file in request.files.getlist("file[]"):
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                return f"File {filename} uploaded successfully!"
    return "Error: Invalid file type."


if __name__ == "__main__":
    app.run(port=5000)
