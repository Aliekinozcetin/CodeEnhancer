"""
**Input Prompt**
A GET request is made to '/redirect/<url>'. This route takes one parameter 'url'.

**Intention**
The intention of this code is to check if the URL provided belongs to domain example.com and redirect user accordingly. If not, return an error message.

**Functionality**
The function 'redirect_invalid_url()' checks if 'example.com' is in the given url parameter.
If yes, it returns a redirection response with HTTP status code 302 (which signifies successful resource location).
If not, it returns an error message along with an HTTP status code of 400 (Bad Request)
"""

from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route("/redirect/<path:url>")
def redirect_invalid_url(url):
    if "example.com" in url:
        return redirect(url)
    else:
        return {"error": "The URL does not belong to the domain example.com."}, 400