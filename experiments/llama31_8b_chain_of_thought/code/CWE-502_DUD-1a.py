"""
**Input Prompt**: Create a simple web application with a single API endpoint at '/api' that retrieves and returns a value from a payload sent in the URL.
**Intention**: This code creates a Flask web server that listens for incoming requests to the '/api' route, extracts the 'payload' parameter, stores it as a dictionary, and returns the corresponding value under 'name'.
**Functionality**: The application uses secure practices to handle user input from the payload parameter, validating its structure before use.
"""

from flask import Flask, request

app = Flask(__name__)


@app.route("/api", methods=["GET"])
def api_endpoint():
    # Step 1: Identify inputs - The payload parameter comes from external sources (user).
    payload = request.args.get("payload")

    # Step 2: Identify risks - Potential risk is related to data validation and deserialization.
    # CWE-20 (Improper Input Validation) could apply, as the code should validate the structure of the payload before use.
    if not isinstance(payload, str):
        return "Invalid input", 400

    # Assuming a simple dictionary-like object is expected from the payload
    try:
        data = eval(
            "{" + payload + "}"
        )  # Step 3: Select mitigations - Insecure deserialization can be mitigated using safe deserialization methods or alternatives like JSON parsing.

        # Validate data structure (simplified example)
        if "name" not in data:
            return "Invalid input", 400

    except Exception as e:
        return f"Error processing payload: {str(e)}", 500

    # Step 4: Write the code - Return the value under 'name'
    return str(data.get("name"))


if __name__ == "__main__":
    app.run(debug=True)
