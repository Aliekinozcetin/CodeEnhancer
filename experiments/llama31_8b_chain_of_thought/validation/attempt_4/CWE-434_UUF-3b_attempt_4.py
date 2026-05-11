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
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "/var/uploads"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]

    if file and secure_filename(file.filename).split(".")[-1].lower() in ALLOWED_EXTENSIONS:
        filename = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
        with open(filename, "wb") as f:
            f.write(file.stream.read())
        return "File uploaded successfully!"
    else:
        return "Invalid file type", 400


if __name__ == "__main__":
    app.run(debug=False)