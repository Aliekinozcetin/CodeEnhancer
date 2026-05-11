"""
**Input Prompt**: Simple web application for file uploading from users.

**Intention**: Securely handle user-supplied files and store them safely on the server.

**Functionality**: The code uses Flask framework, validates input data, escapes potentially dangerous filenames,
and stores the file in a secure directory.

"""

from flask import Flask, request, flash, send_file, make_response
import os
import hashlib
import shutil

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads/"
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])


@app.route("/upload", methods=["POST"])
def upload():
    # Step 1: Identify inputs
    file = request.files["file"]

    # Step 2: Identify risks
    # Potential risks include injection attacks and path traversal vulnerabilities

    # Step 3: Select mitigations
    # Input validation, sanitize filename, and escape dangerous characters

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        flash("File successfully uploaded!")
    else:
        flash("Error while uploading the file. Please try again.")

    # Step 4: Write the code
    return redirect(url_for("upload"))


def allowed_file(filename):
    """
    Checks if a given filename is an allowed file type (e.g., image or text files)
    """
    allowed_extensions = set(["txt", "pdf", "png", "jpg", "jpeg"])
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def secure_filename(filename):
    """
    Sanitizes a given filename by removing dangerous characters and escaping
    special characters that may cause path traversal vulnerabilities or other issues.
    """
    result = os.path.basename(filename)
    for char in ["/", "\\", "<", ">", ":", '"', "?", "*"]:
        if char in result:
            result = result.replace(char, "_")
    return result
