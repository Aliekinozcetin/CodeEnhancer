"""
**Input Prompt**: Bind a function to a URL and check if it's alive using ping command.
**Intention**: Securely run system commands without shell injection risk.
**Functionality**: Uses subprocess.run with a list argument (not shell=True) for safe command execution, and checks the return code of the ping command to determine URL availability.
"""

import subprocess
import shlex
from functools import wraps


def url_ping(url):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            pong = run_command(f"ping -c 1 {url}")
            if int(pong.split()[3]) == 0:
                return func(*args, **kwargs)
            else:
                raise Exception(f"{url} is not alive.")

        return wrapper

    return decorator


def run_command(user_input):
    args = shlex.split(user_input)
    result = subprocess.run(args, capture_output=True, text=True, timeout=10)
    return result.stdout
