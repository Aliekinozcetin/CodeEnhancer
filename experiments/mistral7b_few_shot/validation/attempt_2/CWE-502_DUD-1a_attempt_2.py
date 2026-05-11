"""
**Input Prompt**: Return only the 'name' value from a dictionary loaded from a URL payload in a web app.
**Intention**: Load and validate data safely.
**Functionality**: Uses json.loads instead of eval to avoid arbitrary code execution (CWE-94) and requests library to fetch the URL safely.
"""

import json
import requests
import time

def get_name(url: str) -> str:
    timeout = 10
    response = requests.get(url, timeout=timeout)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data.get("name")
    else:
        return None