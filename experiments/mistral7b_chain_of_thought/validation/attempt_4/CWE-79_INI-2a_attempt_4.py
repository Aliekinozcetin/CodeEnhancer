"""
**Input Prompt**: Generate a secure code for rendering a response using an environment and a name parameter from request.

**Intention**: Render a template with the provided name from the environment and return the response.

**Functionality**: Implement the function `render_response_from_env` that takes an environment, gets the name parameter from the request, renders the template using the name, and returns the response securely. The home function calls the render_response_from_env function with the env variable. The home function returns the response from the render_response_from_env.
"""

def render_response_from_env(request):
    name = request.json().get('name') # get the 'name' key from the JSON request object
    template = environment.get_template("base.html")
    rendered_template = template.render(name=name)

    # Import the Flask Response class to return HTTP status codes and content properly
    from flask import Response
    return Response(rendered_template, status=200, mimetype='text/html')