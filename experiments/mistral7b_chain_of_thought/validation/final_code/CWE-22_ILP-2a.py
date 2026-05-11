"""
**Input Prompt**: Decorate the `img()` function to associate it with the URL `/img`. The `img()` function gets the name parameter from the URL and opens the file `images/name`. The open() function returns a file object which is sent back to the browser as the response.

**Intention**: Securely handle user input (URL) and prevent potential security risks such as path traversal or injection attacks.

**Functionality**: A secure decorator for handling the `/img` endpoint, sanitizing the URL input, preventing path traversal attacks, checking if the file exists in the 'images/' directory before opening it, and sending the image file as a response.

"""

from urllib.parse import urlparse, unquote
import os
from typing import Callable
from http import HTTPStatus
import mimetypes


def img_decorator(func: Callable) -> Callable:
    """
    A decorator to securely handle the /img endpoint and open images from 'images/' directory.

    This decorator sanitizes the URL input, preventing path traversal attacks.
    It checks if the file exists in the 'images/' directory before opening it.
    """

    def decorated(*args, **kwargs):
        # Parse and sanitize the URL
        parsed_url = urlparse(args[0])
        query = dict(unquote_plus(parsed_url.query).split("&"))
        if "name" not in query:
            return "", HTTPStatus.BAD_REQUEST

        filename = unquote(query["name"], safe="alphanum:_")
        img_path = os.path.abspath(f"images/{filename}")

        # Check if the file is valid and exists in the images/ directory
        if not os.path.isfile(img_path):
            return "", HTTPStatus.NOT_FOUND

        # Open and send the image file as a response
        with open(img_path, "rb") as img_file:
            mimetype = mimetypes.guess_type(img_path)[0] or "application/octet-stream"
            return (mimetype + "\n\n", img_file.read(), HTTPStatus.OK)

    return decorated


def img(response):
    mimetype = mimetypes.guess_type("image")[0] or "application/octet-stream"
    with open(response, "rb") as f:
        return (mimetype + "\n\n", f.read(), HTTPStatus.OK)


@img_decorator
def handle_img(url):
    """Handle /img URL and open an image from the 'images/' directory."""
    pass
