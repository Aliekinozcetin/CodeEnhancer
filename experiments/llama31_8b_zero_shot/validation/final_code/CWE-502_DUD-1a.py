"""
**Input Prompt**:
Create a simple web app that has an API endpoint at "/api" which accepts a payload parameter in its URL, stores it as a dictionary and then retrieves and returns the "name" key's value.

**Intention**:
This code serves as a basic demonstration of creating a simple API endpoint to handle data from GET requests.

**Functionality**:
The following Python code uses Flask to create a web application. It defines an API route at "/api", which accepts a URL parameter named 'payload'. The payload is then converted into a dictionary and the 'name' value is returned.
"""

from flask import Flask, request

app = Flask(__name__)


@app.route("/api", methods=["GET"])
def api_endpoint():
    data_dict = dict(request.args)
    return f"Name: {data_dict.get('name')}" if 'name' in data_dict else ""


if __name__ == "__main__":
    app.run(debug=False)