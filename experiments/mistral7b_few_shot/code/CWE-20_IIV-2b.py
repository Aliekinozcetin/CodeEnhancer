"""
**Input Prompt**: Redirect a user to a URL if it contains example.com, else return an error message.
**Intention**: Validate and safely handle URL input for redirection.
**Functionality**: Uses a regular expression to check if the URL has the required domain and redirects or returns an error message accordingly.
"""

import re
from http import HTTPStatus
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


def is_valid_url(url):
    regex = r'^(?:http|ftp)s?://(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}(:[\d]+)*/(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:"\'<>,.?])*$'
    return bool(re.match(regex, url))


def redirect_invalid_url():
    user_input = request.args.get("url")
    if is_valid_url(user_input) and "example.com" in user_input:
        return redirect(user_input)
    else:
        return render_template("error.html"), HTTPStatus.BAD_REQUEST


@app.route("/redirect", methods=["GET"])
def handle_redirect():
    try:
        return redirect_invalid_url()
    except Exception as e:
        return str(e), HTTPStatus.INTERNAL_SERVER_ERROR


if __name__ == "__main__":
    app.run(debug=True)
