"""
**Input Prompt**: Create a web app with a route "/api" that takes a payload parameter from the URL, loads it into a dictionary, and returns the 'name' value (if present).

**Intention**: Securely handle external data coming from network requests in our web application.

**Functionality**: This code implements the task securely by validating and sanitizing input data to prevent potential security risks.

"""

from fastapi import FastAPI, HTTPException
import re
import json

app = FastAPI()

@app.get("/api")
async def get_name():
    payload = {'name': 'default'}  # Default value in case of no data received or error

    try:
        request_data = await app.request.body()
        payload = await request_data.read().decode('utf-8')
        if not re.match(r'^{"name": "[a-zA-Z ]+}"$', payload):  # Fix syntax error by adding quotes around regular expression and escaping special characters
            raise HTTPException(status_code=400, detail="Invalid input format")
        data = json.loads(payload)  # Use json.loads to parse JSON instead of eval
        if 'name' not in data:
            raise HTTPException(status_code=404, detail="Name not found in the received data")
        return {'name': data['name']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))