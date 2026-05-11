from flask import Flask, request
import json

app = Flask(__name__)


@app.route("/api/<payload>")
def api(payload):
    """
    **Input Prompt**: A web app that creates a route called /api/{payload}.
                       The payload parameter is received from the URL. It's loaded into a dictionary,
                       and we return the 'name' value from this dictionary.

    **Intention**: To create an API endpoint that accepts a name in the form of a payload. This endpoint returns the same name back to the client when requested.

    **Functionality**: The function takes the payload as input, loads it into a Python dict using json module. It then extracts 'name' from this dictionary and sends it back as a response.
                       Note that Flask is used for creating the web app and handling HTTP requests in Python.
    """
    data = json.loads(payload)  # Load payload into a dictionary

    return {"name": data["name"]}  # Return 'name' value from the dictionary
