"""
**Input Prompt**: The Python script is designed to handle HTTP GET requests with a URL parameter from an endpoint.
**Intention**: To securely redirect the user to a valid URL if it belongs to 'example.com', else returning an error message.
**Functionality**: This code uses Flask, urllib and flask methods (redirect, url_for, abort) for redirection logic, validation of URL and error handling. It ensures that the provided URL has a scheme(http/https), if not it adds one and then checks again to validate domain.
"""

from urllib.parse import urlparse
from flask import Flask, redirect, abort
app = Flask(__name__)

@app.route('/redirect/<path:url>', methods=['GET'])
def handle_request(url):
    parsed_uri = urlparse(url)
    if not (parsed_uri.scheme and parsed_uri.netloc): # check for scheme, netloc missing
        url = 'http://' + url  # add http to make it valid
        parsed_uri = urlparse(url)
    if not is_valid_domain(parsed_uri.netloc):
        abort(403)
    return redirect(url, code=302)

def is_valid_domain(hostname: str) -> bool:
    """Determines whether the domain of a URL points to 'example.com'."""
    return hostname == "www.example.com" or hostname == "example.com"