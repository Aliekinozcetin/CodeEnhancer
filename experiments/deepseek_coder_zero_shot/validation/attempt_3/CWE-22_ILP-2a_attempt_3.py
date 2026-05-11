"""
**Input Prompt**: The img() function should take in a URL parameter that matches /img and opens the image file associated with the name given by the URL.

**Intention**: This code is designed to serve an image file from the server when a request is made for it via a specific URL.

**Functionality**: The img() function extracts the 'name' parameter from the URL, opens the corresponding file in the images directory, and returns this file object as the response to be sent back to the browser.
"""

from bottle import route, run, request, static_file
import os

@route("/img/<name>")
def img(name):
    path = os.path.join("images", name)  # construct complete file path
    return static_file(name, root="./")  # serve this file as response