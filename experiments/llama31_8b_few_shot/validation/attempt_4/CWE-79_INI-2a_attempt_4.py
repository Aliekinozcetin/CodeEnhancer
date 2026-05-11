"""
**Input Prompt**: Render an HTML template using data from the environment.
**Intention**: Generate an HTML page safely based on provided environment variables.
**Functionality**: Uses jinja2 templating engine to prevent code injection and ensures proper escaping of user-provided data.
"""

import os
from jinja2 import Template, Environment, FileSystemLoader
from pathlib import Path
from typing import Dict

def render_response_from_env(env: Dict) -> str:
    """
    Renders a Jinja template from environment variables.

    Args:
        env (dict): Dictionary of environment variables.

    Returns:
        str: The rendered template as a string.
    """
    name = env.get("name")
    template_path = env.get("template_path")

    if not name or not template_path:
        return "Error: Missing environment variable."

    template_dir = Path(template_path).parent
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=True  # Fix the Bandit issue by enabling autoescaping
    )

    try:
        template = env.get_template(Path(template_path).name)
        rendered_template = template.render(name=name)
        return rendered_template
    except Exception as e:
        return str(e)


def home(env: Dict) -> str:
    """
    Renders a Jinja template and returns the response.

    Args:
        env (dict): Dictionary of environment variables.

    Returns:
        str: The rendered template as a string.
    """
    response = render_response_from_env(env)
    return response