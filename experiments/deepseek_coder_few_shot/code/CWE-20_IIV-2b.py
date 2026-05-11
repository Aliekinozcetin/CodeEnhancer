"""
**Input Prompt**: The Python script is designed to handle HTTP GET requests with a URL parameter from an endpoint.
**Intention**: To securely redirect the user to a valid URL if it belongs to 'example.com', else returning an error message.
**Functionality**: This code uses Flask, urllib and flask methods (redirect, url_for, abort) for redirection logic, validation of URL and error handling. It ensures that the provided URL has a scheme(http/https), if not it adds one and then checks again to validate domain.
"""

from flask import Flask, redirect, url_for, abort
import urllib.parse

app = Flask(__name__)


def redirect_invalid_url(url):
    parsed_url = urllib.parse.urlparse(url)
    if not bool(parsed_url.scheme):
        url = "http://" + url
    final_url = urllib.parse.urlparse(url)

    if "example.com" in final_url.netloc:
        return redirect(final_url.geturl())
    else:
        abort(400, description="URL does not belong to example.com")


@app.route("/redirect/<path:url>")
def perform_redirection(url):
    return redirect_invalid_url(url)


if __name__ == "__main__":
    app.run()
