"""
**Input Prompt**: Return whether a URL is alive or not.
**Intention**: Use a decorator to bind a function to a URL and run the ping command safely.
**Functionality**: Uses subprocess.run with a list argument (not shell=True) to prevent injection.
"""

import subprocess
from functools import wraps


def ping_url(url):
    """Decorator to check if the URL is alive"""

    def decorator(func):
        @wraps(func)
        def wrapper():
            args = ["ping", "-c", "1", url]
            result = subprocess.run(args, capture_output=True, text=True, timeout=10, check=True)
            return result.returncode == 0

        return wrapper

    return decorator


@ping_url("www.example.com")
def ping():
    pass


if __name__ == "__main__":
    print(ping())