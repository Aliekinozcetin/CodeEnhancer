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
import subprocess  # Import this at the top


def ping_check(url):
    """
    Check if a URL is alive by pinging it.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if the URL responds, False otherwise.
    """
    try:
        output = subprocess.check_output(["ping", "-c", "1", url])
    except subprocess.CalledProcessError as e:
        return False

    # Check for a specific error message indicating the URL is down
    if b"0 packets received" in e.output:
        return False
    else:
        return True


@ping_check
def app(url="https://www.example.com"):
    """
    Test if a URL is alive by pinging it.

    Args:
        url (str): The URL to check. Defaults to https://www.example.com.
    """
    if url:
        status = ping_check(url)
        print("URL is alive" if status else "URL is not alive")


app()