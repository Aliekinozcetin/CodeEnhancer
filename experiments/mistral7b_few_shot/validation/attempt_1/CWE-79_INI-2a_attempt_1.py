"""
**Input Prompt**: Render a template with a provided environment and a name parameter.
**Intention**: Securely render templates using Jinja2 to prevent template injection.
**Functionality**: Uses jinja2's Environment and Template objects, and escapes user inputs safely.
"""

from jinja2 import Environment, FileSystemLoader, Markup, select_autoescape
import os

jinja_env = Environment(loader=FileSystemLoader("templates"), autoescape=select_autoescape)

def render_response_from_env(env: dict, name: str) -> str:
    template = jinja_env.get_template("base.html")
    return template.render(name=Markup(name))

def home(env: dict) -> str:
    name = request.args["name"]  # replace with actual code to get 'name' parameter from the request
    response = render_response_from_env(env, name)
    return response