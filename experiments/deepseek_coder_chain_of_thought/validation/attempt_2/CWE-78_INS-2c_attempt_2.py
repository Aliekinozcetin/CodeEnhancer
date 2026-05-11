"""
    **Input Prompt**: A URL to be pinged. The url is stored in a global variable at the start of this script.

    **Intention**: To check if a given URL is alive (reachable) by sending an ICMP echo request using the system command "ping". If the return code is 0, then the URL is considered to be alive.

    **Functionality**: The 'ping' function uses the os module in Python to run system commands. It sends a ping request to the provided url and stores the result of the command execution in the variable "pong". If the return code (stored in pong[2]) is 0, then the URL is considered alive.
    """

import os
from flask import Flask, request

app = Flask(__name__)
url = "http://example.com"    # Input

@app.route("/ping", methods=["GET"])
def ping():
    global url
    if "url" in request.args:
        url = request.args["url"]

    pong = os.system(f'ping -c 1 {url}')
    
    if pong == 0:
        return f"{url} is alive", 200
    else:
        return f"{url} is not alive", 500