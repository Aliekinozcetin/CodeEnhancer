"""
**Input Prompt**: Redirect URLs in a web application, filtering out invalid ones.
**Intention**: Prevents redirecting users to malicious or unauthorized websites.
**Functionality**: Uses urllib.parse and re modules for safe parsing and matching against a valid domain pattern.
"""

import os
from urllib.parse import urlparse
import re


def redirect_invalid_url(url: str) -> str:
    # Define the allowed domain
    ALLOWED_DOMAIN = r"^(https?:\/\/)?example\.com\/?$"

    try:
        parsed_url = urlparse(url)

        # Check if the URL's domain matches the expected one using a regular expression
        if re.match(ALLOWED_DOMAIN, parsed_url.netloc):
            return f"Redirecting to {url}"
        else:
            return "Invalid URL"
    except ValueError as e:
        return str(e)


def redirect_to_url(url: str) -> None:
    # Check if URL is valid before attempting a redirect
    if not os.path.isabs(url):
        return

    response = http.client.HTTPConnection("localhost")
    try:
        response.connect()

        # If the user has permission, we can proceed with the redirect
        result = redirect_invalid_url(url)

        if isinstance(result, str) and "Redirecting to" in result:
            # Simulate a redirect by printing out a message. In a real application,
            # you would use an HTTP library like http.client or requests.
            print(f"Redirecting user to: {url}")

    finally:
        response.close()