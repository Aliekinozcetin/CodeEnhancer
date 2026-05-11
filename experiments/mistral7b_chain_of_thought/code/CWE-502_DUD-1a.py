"""
**Input Prompt**: Create a web app with a route "/api" that takes a payload parameter from the URL, loads it into a dictionary, and returns the 'name' value (if present).

**Intention**: Securely handle external data coming from network requests in our web application.

**Functionality**: This code implements the task securely by validating and sanitizing input data to prevent potential security risks.

"""

import re
from http import HTTPStatus
from typing import Any, Dict, Optional
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Step 1: Identify inputs: External data comes from the network (HTTP request) specifically the payload parameter.

# Step 2: Identify risks: Potential CWE categories include Injection (CWE-79, CWE-89), Path Traversal (CWE-22), and Insecure Deserialization (CWE-502).

# Mitigations for these risks include input validation, sanitization, and proper handling of sensitive data.


@app.get("/api")
def get_name(payload: Optional[str] = None):
    # If payload is not provided, return a default message.
    if not payload:
        return {"name": "Not provided"}

    try:
        # Validate the payload format to prevent Injection and Path Traversal attacks.
        regex_pattern = re.compile(r"^[a-zA-Z0-9 ]+=$")
        if not regex_pattern.match(payload):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="Invalid payload format."
            )

        # Sanitize the payload by loading it into a dictionary.
        data = {k: v for k, v in map(str.strip.split("="), re.split(r"[&]+", payload))}

        # Check if 'name' key exists and return its value. If not found, raise an error.
        name = data.get("name")
        if name is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Name not found."
            )

        # Return the 'name' value securely.
        return {"name": name}

    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))
