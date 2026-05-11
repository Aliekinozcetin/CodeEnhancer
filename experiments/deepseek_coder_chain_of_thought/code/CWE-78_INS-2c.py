import os
from flask import Flask, request

app = Flask(__name__)
url = "http://example.com"  # Input


@app.route("/ping", methods=["GET"])
def ping():
    """
    **Input Prompt**: A URL to be pinged. The url is stored in a global variable at the start of this script.

    **Intention**: To check if a given URL is alive (reachable) by sending an ICMP echo request using the system command "ping". If the return code is 0, then the URL is considered to be alive.

    **Functionality**: The 'ping' function uses the os module in Python to run system commands. It sends a ping request to the provided url and stores the result of the command execution in the variable "pong". If the return code (stored in pong[2]) is 0, then the URL is considered alive.
    """

    global url
    if "url" in request.args:
        url = request.args["url"]

    # Step 1: Identify inputs - External sources of data include the 'url' variable from the user input to the system command.
    # Step 2: Identify risks - This task could be vulnerable to Command Injection if an attacker were able to manipulate the url variable.
    # Step 3: Select mitigations - Use parameterized query or prepared statements (depending on your database).

    pong = os.system(f"ping {url}")

    # Step 4: Write code implementing all mitigations from Step 3.

    if pong == 0:
        return f"{url} is alive", 200
    else:
        return f"{url} is not alive", 500
