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

    if not isinstance(payload, str):
        return "Invalid input", 400

    try:
        data: Dict = json.loads(payload)
        
        if "name" not in data:
            return "Invalid input", 400
    except ValueError as e:
        return f"Error processing payload: {str(e)}", 500

    return str(data.get("name"))


if __name__ == "__main__":
    app.run(debug=False) # Disable debug mode to avoid exposing Werkzeug debugger and allowing arbitrary code execution