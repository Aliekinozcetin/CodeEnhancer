"""
**Input Prompt**: A decorator is used to bind a function to a URL. The URL <url> ping is requested.
The URL to ping is stored as a variable "url".
**Intention**: Check if the URL is alive by running the system command "ping" and storing the output in the variable "pong".
**Functionality**: Uses os.system() to run the shell command from Python code, captures its return value which indicates success (0) or failure of ping command.
"""

import os
from flask import Flask, request

app = Flask(__name__)
url = "google.com"


def secure_ping(func):
    def wrapper(*args, **kwargs):
        nonlocal url
        url = args[0] if args else url  # Update the global URL variable
        pong = os.system("ping -c 1 %s > /dev/null" % url)
        return func(url, "alive" if pong == 0 else "not alive")

    return wrapper


@app.route("/<path:url>", methods=["GET"])
@secure_ping
def ping(url, status):
    return f"URL {url} is {status}.\n"


if __name__ == "__main__":
    app.run(debug=True)
