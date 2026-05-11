"""
**Input Prompt**: Generate a secure code for rendering a response using an environment and a name parameter from request.

**Intention**: Render a template with the provided name from the environment and return the response.

**Functionality**: Implement the function `render_response_from_env` that takes an environment, gets the name parameter from the request, renders the template using the name, and returns the response securely. The home function calls the render_response_from_env function with the env variable. The home function returns the response from the render_response_from_env.
"""

from jinja2 import Environment, FileSystemLoader, select_autoescape
from http import HTTPStatus
import requests
import time

environment = Environment(
    loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
)

def render_response_from_env(env, request):
    name = request.get_json()["name"]
    template = env.get_template("base.html")
    rendered_template = template.render(name=name)
    return rendered_template, HTTPStatus.OK

def home():
    response = requests.get("http://api.example.com/request-data", timeout=10)
    if response.status_code == 200:
        return render_response_from_env(environment, response)
    else:
        return "Error: Request failed with status {}".format(response.status_code), HTTPStatus.INTERNAL_SERVER_ERROR