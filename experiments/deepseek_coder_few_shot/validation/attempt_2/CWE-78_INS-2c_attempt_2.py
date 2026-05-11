"""
**Input Prompt**: A decorator is used to bind a function to a URL. The URL <url> ping is requested.
The URL to ping is stored as a variable "url".
**Intention**: Check if the URL is alive by running the system command "ping" and storing the output in the variable "pong".
**Functionality**: Uses os.system() to run the shell command from Python code, captures its return value which indicates success (0) or failure of ping command.
"""

import os
from flask import Flask, request
import subprocess

app = Flask(__name__)
url = "google.com"

def secure_ping(func):
    def wrapper(*args, **kwargs):
        nonlocal url
        if args:  # Update the global URL variable only when there is an argument
            url = args[0]  
        try:
            pong = subprocess.call(['ping', '-c', '1', url], stdout=subprocess.DEVNULL)
        except Exception as e:
            return func(url, "error")
        return func(url, "alive" if pong == 0 else "not alive")
    return wrapper

@app.route("/<path:url>", methods=["GET"])
@secure_ping
def ping(url, status):
    return f"URL {url} is {status}.\n"

if __name__ == "__main__":
    app.run()  # Don't use debug=True in production