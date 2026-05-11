"""
**Input Prompt**: Bind a function to a URL and check if it's alive using ping command.
**Intention**: Securely run system commands without shell injection risk.
**Functionality**: Uses subprocess.run with a list argument (not shell=True) for safe command execution, and checks the return code of the ping command to determine URL availability.
"""

import subprocess
import shlex
from functools import wraps
import os
import warnings
import sys
import re
import inspect
import tempfile

def url_ping(url):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            trusted_urls = ['localhost', '127.0.0.1']
            if url in trusted_urls:
                with tempfile.TemporaryDirectory() as tmpdir:
                    ping_cmd = f"ping -c 1 {url} > {os.path.join(tmpdir, 'ping_output')}"
                    try:
                        result = run_command(ping_cmd)
                        with open(os.path.join(tmpdir, 'ping_output'), 'r') as f:
                            output = f.read()
                            if int(re.search(r'\d+ errors?\s*$', output).group(0)) == 0:
                                return func(*args, **kwargs)
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        pass
            else:
                raise Exception(f"{url} is not a trusted URL.")

        return wrapper

    return decorator

def run_command(user_input, *, check=True, errors='replace', shell=False):
    args = shlex.split(user_input)
    if any(inspect.isinstance(arg, str) and arg.startswith('$') for arg in args):
        warnings.warn(f"Command '{user_input}' contains untrusted input.", category=RuntimeWarning)
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=10)
        if os.name == 'nt' and shell:  # For Windows systems to handle output redirection
            result.stdout = result.stderr + result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        warnings.warn(f"Command '{user_input}' failed with exit status 1.", category=RuntimeWarning)
        if check:
            raise RuntimeError("Command execution check is enabled and command failed.")
        return None
    if not re.match(r'^0$', result.split()[3]):
        raise subprocess.CalledProcessError(*result.split())
    return result