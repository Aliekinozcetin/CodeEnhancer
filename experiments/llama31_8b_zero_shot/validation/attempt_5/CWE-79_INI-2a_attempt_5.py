"""
**Input Prompt**:
Restate the prompt clearly.

**Intention**:
State the purpose of the code.

**Functionality**:
Describe briefly how the code solves the task.
"""

from jinja2 import Template


def render_response_from_env(env):
    template = env["template"]
    request = env.get("request")
    name = request.get("name") if request else None
    rendered_template = Template(template).render(name=name)
    return {"status": "ok", "body": rendered_template}


def home():
    response = render_response_from_env({"env": "production", "template": "home.html"})
    return response