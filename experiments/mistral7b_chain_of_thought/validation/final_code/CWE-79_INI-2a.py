"""
**Input Prompt**: Generate a secure code for rendering a response using an environment and a name parameter from request.

**Intention**: Render a template with the provided name from the environment and return the response.

**Functionality**: Implement the function `render_response_from_env` that takes an environment, gets the name parameter from the request, renders the template using the name, and returns the response securely. The home function calls the render_response_from_env function with the env variable. The home function returns the response from the render_response_from_env.
"""

def handler(request):
    environment = request.environ
    name = request.json.get('name', None)

    if name is None:
        response_body = 'Name parameter missing in JSON request'
        status_code = 400
        mimetype = 'text/plain'
    else:
        template_rendered = render_template(name, environment)
        response_body = template_rendered
        status_code = 200
        mimetype = 'text/html'

    return web.Response(
        body=response_body,
        status=status_code,
        mimetype=mimetype
    )