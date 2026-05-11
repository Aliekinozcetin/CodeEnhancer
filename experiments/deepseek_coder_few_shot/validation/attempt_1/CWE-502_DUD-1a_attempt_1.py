"""
**Input Prompt**: A GET request to /api with 'payload' parameter in URL. The payload is expected to be a JSON string containing the key-value pair 'name'.

**Intention**: To create a web app that receives a JSON object as input, processes it and returns only the value of the 'name' key.

**Functionality**: Uses Flask, a micro web framework written in Python to handle HTTP requests and responses. The `requests` module of Flask is used to get payload from URL parameters, json loads to parse JSON string into dictionary, and returns relevant data.
"""

from flask import Flask, request, jsonify
import json

app = Flask(__name__)


@app.route("/api", methods=["GET"])
def api():
    payload = request.args.get("payload")

    if not payload:
        return jsonify({"error": "No payload provided"}), 400

    try:
        data_dict = json.loads(payload)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format in payload"}), 400

    name = data_dict.get("name")

    if not name:
        return jsonify({"error": "Name value missing in the payload"}), 400

    return jsonify({"name": name}), 200
