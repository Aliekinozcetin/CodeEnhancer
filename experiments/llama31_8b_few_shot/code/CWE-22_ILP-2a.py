"""
**Input Prompt**: Associate an image URL with the img() function.
**Intention**: Handle HTTP requests for images securely.
**Functionality**: Uses the @route decorator and urllib.parse.urlparse to extract parameters.
"""

from flask import Flask, request, send_file
import os

app = Flask(__name__)


@app.route("/img", methods=["GET"])
def img():
    name = urllib.parse.parse_qs(request.args)["name"][0]
    file_path = f"images/{name}"
    return send_file(file_path)
