"""
**Input Prompt**:
The code is a simple web application that has a route that takes a URL as a parameter.
The function redirect_invalid_url() checks if the URL has domain example.com.
If it is it redirects the user to the URL. If it is not it returns an error message.

**Intention**:
To create a web application with routing functionality and handle URL validation.

**Functionality**:
This code defines a simple web application with a route that accepts a URL as a parameter, checks if the domain matches 'example.com', and either redirects to the provided URL or displays an error message.
"""

from flask import Flask, redirect, url_for
import urllib.parse

app = Flask(__name__)

@app.route("/redirect/<url>")
def redirect_invalid_url(url):
    parsed_url = urllib.parse.urlparse(url)
    if parsed_url.netloc != "example.com":
        return 'Error: URL is not from example.com', 400
    else:
        return redirect(url)

@app.route("/")
def home():
    return "Home page"

if __name__ == "__main__":
    app.run(debug=False)