"""**Input Prompt**: The task is to create a web app that loads the payload parameter from URL and returns the name value from the dictionary.

    **Intention**: This code serves as an example of secure coding practices by using Flask, urllib.parse for url parsing, and returning values from a dictionary based on user input in the URL.

    **Functionality**: The function 'api' handles HTTP GET requests at /api route. It uses urlencode to parse the payload parameter from the URL into a dictionary. Then it returns the name value from this dictionary.
    """

from flask import Flask, request, jsonify
import urllib.parse   # for url parsing

app = Flask(__name__)

@app.route("/api", methods=['GET'])
def api():
    payload = request.args.get("payload") 
    
    if not payload:
        return jsonify({"error": "No payload provided in URL"}), 400
        
    parsed_dict = urllib.parse.unquote(urllib.parse.unquote(payload))   # url parsing should be done securely
    
    return_dict = {}
    for entry in parsed_dict.split("&"):
        key, value = entry.split("=")
        return_dict[key] = urllib.parse.unquote(value)   # ensure that only valid data is processed by unquoting the values
    
    if "name" not in return_dict:
        return jsonify({"error": "No 'name' key in payload dictionary"}), 400
        
    return jsonify({"name": return_dict["name"]})   # return JSON response with name value from the dictionary