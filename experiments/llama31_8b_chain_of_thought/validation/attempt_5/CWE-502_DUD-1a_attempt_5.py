"""
**Input Prompt**: Create a simple web application with a single API endpoint at '/api' that retrieves and returns a value from a payload sent in the URL.
**Intention**: This code creates a Flask web server that listens for incoming requests to the '/api' route, extracts the 'payload' parameter, stores it as a dictionary, and returns the corresponding value under 'name'.
**Functionality**: The application uses secure practices to handle user input from the payload parameter, validating its structure before use.
"""

from flask import Flask, request
import json
from typing import Dict

app = Flask(__name__)


@app.route("/api", methods=["GET"])
def api_endpoint():
    payload = request.args.get("payload")

    try:
        data: Dict = json.loads(payload)
        
        if "name" not in data:
            return "Invalid input", 400
    except ValueError as e:
        return f"Error processing payload: {str(e)}", 500

    # Check if 'data' is a dictionary before accessing its keys
    if isinstance(data, dict):
        return str(data.get("name"))