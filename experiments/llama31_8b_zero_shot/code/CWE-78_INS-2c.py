"""
**Input Prompt**:
A decorator is used to bind a function to a URL.
The function ping() is called when the URL <url> ping is requested.
The URL to ping is stored as a variable "url".
The ping command is run using the system command "ping".
The output of the ping command is stored in the variable "pong".
If the ping command returns 0 the URL is alive.
Else the URL is not alive.

**Intention**:
This code uses a decorator to create a web application that checks if a given URL is alive by pinging it.

**Functionality**:
The code defines a decorator @ping_check that binds a function to a URL and runs the ping command. The result of the ping command is then used to determine whether the URL is alive or not.
"""

import os
from functools import wraps


def ping_check(url):
    pong = os.popen(f"ping {url}").read()
    if "0 packets received" in pong:
        return True
    else:
        return False


@ping_check
def app(url="https://www.example.com"):
    if url:
        status = ping_check(url)
        print("URL is alive" if status else "URL is not alive")


app()
