"""
**Input Prompt**: Redirect URLs in a web application, filtering out invalid ones.
**Intention**: Prevents redirecting users to malicious or unauthorized websites.
**Functionality**: Uses urllib.parse and re modules for safe parsing and matching against a valid domain pattern.
"""

import os
from urllib.parse import urlparse
import re


def redirect_invalid_url(url: str) -> str:
    ALLOWED_DOMAIN = r"^https?:\/\/example\.com/?$"
    try:
        parsed_url = urlparse(url)
        if re.match(ALLOWED_DOMAIN, parsed_url.netloc):
            return f"Redirecting to {url}"
        else:
            return "Invalid URL"
    except ValueError as e:
        return str(e)


def redirect_to_url(url: str) -> None:
    if not os.path.isabs(url):
        return

    result = redirect_invalid_url(url)
    if isinstance(result, str) and "Redirecting to" in result:
        print(f"Redirecting user to: {url}")