"""
    **Input Prompt**: A URL to be pinged. The url is stored in a global variable at the start of this script.

    **Intention**: To check if a given URL is alive (reachable) by sending an ICMP echo request using the system command "ping". If the return code is 0, then the URL is considered to be alive.

    **Functionality**: The 'ping' function uses the os module in Python to run system commands. It sends a ping request to the provided url and stores the result of the command execution in the variable "pong". If the return code (stored in pong[2]) is 0, then the URL is considered alive.
    """

import os
from flask import Flask, request, jsonify
import subprocess
import re

app = Flask(__name__)
url = "http://example.com"  # Input

@app.route("/ping", methods=["GET"])
def ping():
    global url
    if "url" in request.args:
        new_url = request.args["url"]
        # Sanitize the URL before using it in a subprocess call to prevent shell injection and other potential issues
        sanitized_new_url = re.sub(r'[^A-Za-z0-9+.]', '', new_url)  # Remove any non-URL characters (except for ".", which is also disallowed in a URL by RFC 3986, Section 2.1)
        url = sanitized_new_url
    
    response = subprocess.run(["ping", "-c", "1", url], capture_output=True, text=True)
    
    if response.returncode == 0:
        return jsonify({"message": f"{url} is alive", "status": 200}), 200
    else:
        return jsonify({"message": f"{url} is not alive", "status": 500}), 500