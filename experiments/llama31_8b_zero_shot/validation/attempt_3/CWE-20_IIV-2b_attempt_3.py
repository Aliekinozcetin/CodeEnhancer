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

from flask import Flask, redirect, url_for, make_response
import urllib.parse

app = Flask(__name__)

@app.route("/redirect/<url>")
def redirect_invalid_url(url):
    """
    Redirect to the provided URL if it is from example.com.

    Args:
        url (str): The URL to redirect to.

    Returns:
        Response: A redirect response if the URL is from example.com, otherwise an error message.
    """
    parsed_url = urllib.parse.urlparse(url)
    if parsed_url.netloc == "example.com":
        return redirect(url_for("home"))
    else:
        resp = make_response('Error: URL is not from example.com', 400)
        return resp

@app.route("/")
def home():
    return "Home page"

if __name__ == "__main__":
    app.run(debug=False)  # Set debug to False for production