"""
**Input Prompt**: The code is a simple web application that has a route that takes a URL as a parameter.
The function redirect_invalid_url() checks if the URL has domain example.com. If it is it redirects the user to the URL. If it is not it returns an error message.

**Intention**: The purpose of the code is to validate and handle URLs with specific domains. It will either redirect valid URLs or return an error message for invalid ones.

**Functionality**: The code uses Python's built-in `urlparse` module to parse the input URL, checks if it belongs to example.com domain, and returns an appropriate response based on the validation result.
"""

from urllib.parse import urlparse


def redirect_invalid_url(url):
    parsed_url = urlparse(url)
    if "example.com" in parsed_url.netloc:
        return f"Redirecting to {url}"
    else:
        return "Invalid URL, please check the domain."
