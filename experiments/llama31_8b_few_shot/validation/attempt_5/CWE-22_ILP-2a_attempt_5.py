"""
**Input Prompt**: Associate an image URL with the img() function.
**Intention**: Handle HTTP requests for images securely.
**Functionality**: Uses the @route decorator and urllib.parse.urlparse to extract parameters.
"""

from flask import Flask, request, send_file
import os
from urllib.parse import urlparse, parse_qs
from werkzeug.exceptions import NotFound

app = Flask(__name__)

@app.route("/img", methods=["GET"])
def img():
    url_param = request.args.get("url")
    parsed_url = urlparse(url_param)
    query_params = parse_qs(parsed_url.query)
    name = query_params.get("name", [None])[0]
    if name and os.path.exists(os.path.join("images", name)):
        return send_file(os.path.join("images", name))
    else:
        raise NotFound()