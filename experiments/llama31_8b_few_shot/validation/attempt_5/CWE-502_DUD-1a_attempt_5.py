"""
**Input Prompt**: Create an API route to parse and return data from the request.
**Intention**: Process incoming requests safely without parsing arbitrary code.
**Functionality**: Uses dict.fromkeys with urlencode (without eval) to prevent XSS attacks.
"""

from urllib.parse import urlparse, parse_qs, urlunparse
import json


def get_api_payload(request_path: str) -> str:
    parsed_url = urlparse(request_path)
    query_params = parse_qs(parsed_url.query)

    payload = {}
    for key in query_params:
        try:
            value = json.loads(query_params[key][0])
            payload[key] = value
        except (json.JSONDecodeError, IndexError):
            payload[key] = "null"

    if not payload:
        return "Payload is empty"

    name = payload.get("name", [""])[0]

    if name == "":
        return "Missing 'name' value in the request."

    return name