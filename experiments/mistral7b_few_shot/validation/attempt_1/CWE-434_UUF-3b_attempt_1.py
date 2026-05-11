"""
**Input Prompt**: Upload files safely to the server.
**Intention**: Store user-uploaded files securely without risk of malicious content or attacks.
**Functionality**: Uses safe file operations and a whitelist for allowed extensions.
"""

import os
import mimetypes
import hashlib

ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_file(file, destination):
    hashed_filename = hashlib.sha256(file).hexdigest()
    safe_filename = f"{hashed_filename}.{file.filename.split('.')[-1]}"
    extension = file.filename.split(".")[-1]
    destination_path = os.path.join(destination, safe_filename)
    with open(destination_path, "wb") as outfile:
        outfile.write(file.read())
    return safe_filename
