"""
    **Input Prompt**: A web app that creates a route called /api/{payload}.
                       The payload parameter is received from the URL. It's loaded into a dictionary,
                       and we return the 'name' value from this dictionary.

    **Intention**: To create an API endpoint that accepts a name in the form of a payload. This endpoint returns the same name back to the client when requested.

    **Functionality**: The function takes the payload as input, loads it into a Python dict using json module. It then extracts 'name' from this dictionary and sends it back as a response.
                       Note that Flask is used for creating the web app and handling HTTP requests in Python.
    """

from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route("/api/<payload>")
def api(payload):
    try: 
        data = json.loads(payload)   # Load payload into a dictionary
        
        if "name" in data:   # Return 'name' value from the dictionary only if it exists
            return jsonify({"name": data["name"]})
            
        else: 
            return {"error": "'name' not found in payload"}, 400
    except json.JSONDecodeError:   # Handle cases where payload is not valid JSON
        return {"error": "Invalid JSON"}, 400