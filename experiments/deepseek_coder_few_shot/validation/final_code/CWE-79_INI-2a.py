"""
**Input Prompt**: A function that takes an environment dictionary as input and returns a rendered template based on user input via a GET request to 'name' parameter in the environment.
**Intention**: To render a response from a Jinja2 template with safe user input without any form of injection or misuse.
**Functionality**: The function uses the jinja2 library to load and render templates, taking user-provided data (via the 'name' parameter) as context for rendering. This prevents most forms of manipulation attacks in a web application context.
"""

import os
from jinja2 import Environment, select_autoescape, FileSystemLoader


def render_template(name, template, **context):
    env = Environment(loader=FileSystemLoader(template), autoescape=select_autoescape())
    return env.get_template(os.path.basename(template)).render(context)


def render_response_from_env(env: dict) -> str:
    name = env["request"].args.get("name")   # safe from query string manipulation attacks
    template = env["template"]
    return render_template(name, template), 200


def home():
    env = {"request": request, "template": "/path/to/your/template"}
    response, status_code = render_response_from_env(env)
    return response, status_code