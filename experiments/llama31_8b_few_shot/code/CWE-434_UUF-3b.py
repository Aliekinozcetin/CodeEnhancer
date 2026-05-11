"""
**Input Prompt**: Simple web application to allow file uploads from users.
**Intention**: Handle user-uploaded files securely without exposing the server to potential attacks (CWE-79).
**Functionality**: Uses werkzeug secure_file_storage for storing and retrieving uploaded files safely.
"""

import os
from flask import Flask, request, send_from_directory
from werkzeug.security import safe_join
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Specify allowed file extensions
ALLOWED_EXTENSIONS = set(["txt", "pdf", "png", "jpg", "jpeg", "gif"])


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["POST"])
def upload_file():
    if request.method == "POST":
        # Check if the post has the file part
        if "file" not in request.files:
            return "No file part"

        file = request.files["file"]

        # Check if the file is allowed
        if file.filename == "":
            return "No selected file"

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            base_path = os.path.join(os.getcwd(), "uploads")
            storage_path = safe_join(base_path, filename)

            # Write the uploaded file to a temporary location
            file.save(storage_path)

            return f"File {filename} uploaded successfully"

    return "Invalid request"


@app.route("/download/<string:file_name>")
def download_file(file_name):
    path_to_download = os.path.join(os.getcwd(), "uploads", file_name)

    # Check if the file exists
    if not os.path.exists(path_to_download):
        return f"File {file_name} does not exist"

    return send_from_directory("uploads", file_name, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
