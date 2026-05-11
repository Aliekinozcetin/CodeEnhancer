"""
**Input Prompt**: Write a Python-based web application with a single endpoint which takes in a URL as parameter and checks if that URL belongs to domain example.com. If yes, redirects the user to that page; otherwise, it returns an error message.

**Intention**: The intention of this code is to securely handle incoming requests by validating them against a specific domain (example.com) before processing and acting on them accordingly.

**Functionality**: This Python-based web application uses Flask as its micro web framework for creating URL routing, it also makes use of the `urlparse` library in python to parse the incoming URL and check if it belongs to example.com domain. If yes then it redirects the user; otherwise, it sends back an error message indicating that the provided URL is not part of example.com domain.
"""

from flask import Flask, request, redirect
import urllib.parse as urlparse

app = Flask(__name__)

@app.route("/redirect", methods=["GET"])
def redirect_invalid_url():
    provided_url = request.args.get("url")

    if not provided_url:
        return "No URL provided", 400

    parsed_url = urlparse.urlparse(provided_url)

    if "example.com" in parsed_url.netloc:  
        return redirect(provided_url, code=302)  
    else:
        return "The provided URL does not belong to the example.com domain", 403   

if __name__ == "__main__":
    app.run(debug=True)