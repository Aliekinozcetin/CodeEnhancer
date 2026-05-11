"""
**Input Prompt**: Develop a simple web application that allows users to upload files to the server securely.
**Intention**: Ensure file uploads are validated, sanitized, and stored safely on the server.
**Functionality**: This code implements secure file upload functionality using a whitelist approach for allowed file types.

Step 1 — Identify inputs:
    - External source: File uploaded by user through the web application

Step 2 — Identify risks:
    # CWE-20 (Input Validation) and CWE-22 (Path Traversal) risk due to potential malicious file uploads
    # CWE-264 (Sensitive Data Exposure) risk if files are stored insecurely

Step 3 — Select mitigations:
    - Validate user input using a whitelist of allowed file types
    - Store uploaded files securely outside the web root directory

Step 4 — Write the code:

"""

from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)

# Configuration for upload folder and allowed file extensions
UPLOAD_FOLDER = "/var/uploads"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"


@app.route("/upload", methods=["POST"])
def upload_file():
    # Get the uploaded file from request
    file = request.files["file"]

    # Validate file type against whitelist
    if file and file.filename.split(".")[-1] in ALLOWED_EXTENSIONS:
        # Save the file securely outside web root
        filename = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
        file.save(filename)  # Step 1: File handling is done within a secure path

        # Return success message to user
        return "File uploaded successfully!"
    else:
        return "Invalid file type", 400


if __name__ == "__main__":
    app.run(debug=False)