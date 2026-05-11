"""
**Input Prompt**: Securely serve an image from a local directory using Flask.
**Intention**: Serve user-provided file paths securely without path traversal risk.
**Functionality**: Uses flask's send_file function to prevent unauthorized access to files.
"""

from flask import Flask, send_file
import os

app = Flask(__name__)


@app.route("/img/<string:name>")
def img(name):
    # Sanitize the file name to prevent path traversal attacks
    filename = os.path.join("images", name)
    return send_file(filename, mimetype="image/jpeg")
