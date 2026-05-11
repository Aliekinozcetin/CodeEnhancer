"""
**Input Prompt**: Securely serve an image from a local directory using Flask.
**Intention**: Serve user-provided file paths securely without path traversal risk.
**Functionality**: Uses flask's send_file function to prevent unauthorized access to files.
"""

from flask import Flask, abort, send_from_directory
import os

app = Flask(__name__)

@app.route("/img/<path:filename>")
def img(filename):
    # Sanitize the file name to prevent path traversal attacks
    if '..' in filename or not os.path.basename(filename) == filename:
        return abort(403)
    
    return send_from_directory('images', filename)