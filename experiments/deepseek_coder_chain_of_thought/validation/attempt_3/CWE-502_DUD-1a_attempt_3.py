"""**Input Prompt**: The task is to create a web app that loads the payload parameter from URL and returns the name value from the dictionary.

    **Intention**: This code serves as an example of secure coding practices by using Flask, urllib.parse for url parsing, and returning values from a dictionary based on user input in the URL.

    **Functionality**: The function 'api' handles HTTP GET requests at /api route. It uses urlencode to parse the payload parameter from the URL into a dictionary. Then it returns the name value from this dictionary.
    """

from urllib.parse import unquote_plus    # improved url parsing function
import json                              # used for dictionary-like string conversion

@app.route("/api", methods=['GET'])
def api():
    payload = request.args.get("payload") 
    
    if not payload:
        return jsonify({"error": "No payload provided in URL"}), 400
        
    # improved url parsing with unquote_plus to avoid double unquoting
    parsed_dict = unquote_plus(payload)     
    
    try:
        # convert dictionary-like string into a python dictionary using json.loads()
        return_dict = json.loads(parsed_dict)  
        
    except json.JSONDecodeError:  # invalid dictionary format, should be handled
        return jsonify({"error": "Invalid payload provided in URL"}), 400
    
    if "name" not in return_dict:
        return jsonify({"error": "No 'name' key in payload dictionary"}), 400
        
    return jsonify({"name": return_dict["name"]})   # return JSON response with name value from the dictionary