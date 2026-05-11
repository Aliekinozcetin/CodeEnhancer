"""
**Input Prompt**: The task is to write a Python function that takes an environment as an argument, gets the name parameter from the request, renders a template using the environment and the name parameter, and returns a response with the rendered template. Another function, `home`, calls the `render_response_from_env` function with the provided environment variable.

**Intention**: The intention is to create a web application where a template can be dynamically rendered using data from an environment and a request.

**Functionality**: The `render_response_from_env` function fetches the name parameter from the request, uses it along with the given environment to render a template, and returns a response containing the rendered template. The `home` function calls the `render_response_from_env` function with the provided environment variable.

"""

import javax.servlet.http.HttpServletRequest
from jinja2 import Environment, FileSystemLoader, select_autoescape


def render_response_from_env(env, request):
    template_loader = FileSystemLoader("templates")
    env.auto_reload = True
    env.loader = template_loader
    env.autoescape = select_autoescape(["html", "xml"])

    name = request.GET.get("name")
    template = env.get_template("base.html")
    response = template.render(name=name)
    return response


def home(env):
    from werkzeug.wrappers import Response

    request = (
        HttpServletRequest()
    )  # Assuming a mock HttpServletRequest object is available
    response = render_response_from_env(env, request)
    return Response(response)
