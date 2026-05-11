"""
**Input Prompt**: Create a web app that has a route '/api' which takes a payload parameter from the URL, loads it into a dictionary and returns the 'name' value from the dictionary.

**Intention**: To create a simple REST API endpoint that accepts a payload as a parameter in the URL, processes it, and returns a specific value (in this case, the 'name' value).

**Functionality**: The code below creates a Flask web app with one route ('/api'). When a request is made to this route with a query parameter 'payload', the app will parse the payload as JSON, load it into a dictionary, and return the 'name' value from that dictionary.

"""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/api", methods=["GET"])
def get_name():
    payload = request.args.get("payload")
    if payload:
        data = json.loads(payload)
        name = data.get("name")
        return jsonify({"name": name})
    else:
        return jsonify({"error": "No payload provided."}), 400


if __name__ == "__main__":
    app.run(debug=True)
