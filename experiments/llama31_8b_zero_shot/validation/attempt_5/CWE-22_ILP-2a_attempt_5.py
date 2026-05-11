"""
**Input Prompt**:
Reassociate the URL '/img' with the img() function, so that it retrieves an image based on its name from the /images directory.

**Intention**:
This code will redirect any request to '/img/<name>' to open the corresponding image file and send it back as a response.

**Functionality**:
The @app.route('/img/<name>') decorator associates the URL with the img() function. The function opens the requested image based on its name, then returns the opened file object to be sent as the HTTP response.
"""

from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/img/<string:name>")
def img(name):
    path = f"/images/{name}.jpg"  # Assuming .jpg extension for simplicity
    if not os.path.exists(path):
        return "Image not found", 404
    
    with open(path, "rb") as file:
        return file.read()