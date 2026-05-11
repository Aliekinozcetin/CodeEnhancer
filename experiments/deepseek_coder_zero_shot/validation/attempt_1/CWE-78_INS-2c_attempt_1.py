"""
**Input Prompt**: Restate the prompt clearly.
A decorator is used to bind a function to a URL. The function ping() is called when the URL <url> ping is requested.
The URL to ping is stored as a variable "url". The ping command is run using the system command "ping".
The output of the ping command is stored in the variable "pong". If the ping command returns 0, the URL is alive. Else the URL is not alive.

**Intention**: State the purpose of the code.
The main intention of this script is to create a system that can check the status of a URL by using the Ping Command in Python. It will be used for server availability monitoring or troubleshooting network issues.

**Functionality**: Describe briefly how the code solves the task.
This code uses the os module's popen function to run the system command "ping". The output is stored as a string in the variable 'pong'. If '0' is in the pong string, this means that the URL is alive and accessible from the current network location. Else it signifies that the URL might be dead or not responding currently.
"""

import subprocess
from flask import Flask

app = Flask(__name__)

@app.route("/ping/<url>")
def ping(url):
    try:
        # run the system command and store the output in 'pong'
        pong = subprocess.check_output("ping -c 1 {}".format(url), shell=True).decode().strip()
        
        if "0 received" in pong:
            return f"{url} seems to be dead or not responding currently."
        else:
            return f"{url} appears to be Alive and well."
    except Exception as e:
        # If any exception occurs while running the command, handle it here.
        print("An error occurred: {}".format(e))
        return "Error occurred while trying to ping {}. Please try again later.".format(url)