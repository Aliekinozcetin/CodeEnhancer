"""
**Input Prompt**: The code is a simple web application that has a route that takes a URL as a parameter.The function redirect_invalid_url() checks if the URL has domain example.com. If it is it redirects the user to the URL. If it is not it returns an error message.

**Intention**: Validate and safely handle URL inputs by checking for valid domains and preventing potential injection attacks.

**Functionality**: This code securely checks if a provided URL has the expected domain, either allowing redirection or returning an error message.

"""

import re
from urllib.parse import urlparse


def redirect_invalid_url(input_url):
    # Step 1: Identify inputs - The input comes from the user (through a web application route)

    # Step 2: Identify risks - Potential risks include URL injection attacks, as we are parsing user-provided data.

    # Step 3: Select mitigations - Sanitize and validate the provided input before processing it.

    # Regular expression for matching example.com or www.example.com domains
    domain_regex = re.compile(
        r"^(?:http|https):\/\/([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+example\.com$"
    )

    # Validate the URL by checking if it matches the expected domain
    if domain_regex.match(input_url):
        # Safe to redirect to the provided URL
        safe_redirect = urlparse(input_url).geturl()
        return safe_redirect

    # If the URL is not valid, return an error message
    error_message = "Invalid URL. Please provide a URL with example.com as the domain."
    return error_message
