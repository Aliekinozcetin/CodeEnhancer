from flask import Flask, request
import urllib.parse  # for url parsing

app = Flask(__name__)


@app.route("/api")
def api():
    """**Input Prompt**: The task is to create a web app that loads the payload parameter from URL and returns the name value from the dictionary.

    **Intention**: This code serves as an example of secure coding practices by using Flask, urllib.parse for url parsing, and returning values from a dictionary based on user input in the URL.

    **Functionality**: The function 'api' handles HTTP GET requests at /api route. It uses urlencode to parse the payload parameter from the URL into a dictionary. Then it returns the name value from this dictionary.
    """

    # Step 1: Identify inputs
    # Here we have identified the input as a query parameter in the URL.

    payload = request.args.get("payload")

    # Step 2: Identify risks
    # If an attacker is able to control 'payload' parameter from client-side, it may lead to Injection attacks.

    parsed_dict = urllib.parse.unquote(urllib.parse.unquote(payload))

    # Step 3: Select mitigations
    # url parsing should be done securely using urllib.parse which helps in preventing Injection attacks.

    return_dict = {}
    for entry in parsed_dict.split("&"):
        key, value = entry.split("=")
        return_dict[key] = value

    # Step 4: Write the code
    # The payload is split into entries and each entry further splits into a key-value pair using '='. This helps in preventing Injection attacks by ensuring that only valid data is processed.

    return return_dict["name"]
