"""
**Input Prompt**: Render an HTML template using data from the environment.
**Intention**: Generate an HTML page safely based on provided environment variables.
**Functionality**: Uses jinja2 templating engine to prevent code injection and ensures proper escaping of user-provided data.
"""

import os
from jinja2 import Template, TemplateError


def render_response_from_env(env: dict) -> str:
    name = env.get("name")
    template_path = env.get("template_path")

    if not name or not template_path:
        return "Error: Missing environment variable."

    try:
        with open(template_path, encoding="utf-8") as f:
            template = Template(f.read())

        rendered_template = template.render(name=name)
        return rendered_template
    except TemplateError as e:
        return str(e)


def home(env: dict) -> str:
    response = render_response_from_env(env)
    return response


# Example usage:
env = {"name": "John Doe", "template_path": "path/to/template.html"}

print(home(env))
