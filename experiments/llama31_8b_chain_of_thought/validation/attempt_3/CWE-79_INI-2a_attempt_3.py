"""
**Input Prompt**: The `render_response_from_env` function is designed to handle environment variables and generate responses for a web application.
**Intention**: This code aims to securely retrieve template names from the request, render templates with dynamic data, and return HTTP responses.
**Functionality**: It ensures that user-provided input is validated and sanitized before rendering templates to prevent injection attacks. The `home` function serves as an entry point for this process.
"""

def render_response_from_env(env):
    # Step 1: Identify inputs - The name parameter comes from the request, which could be a potential security risk if not properly validated
    name = env["request"].get(
        "name"
    )  # Ensure 'name' is explicitly defined in the request to avoid KeyError

    # Check for potential security risks and sanitize user input using Jinja2's `Markup` class.
    from jinja2 import Markup
    if not isinstance(name, str):
        raise ValueError("Invalid name parameter")
    name = Markup.escape(str(name))

    # Step 3: Select mitigations - Use template engines like Jinja2 that support secure template rendering with safe string filtering
    import jinja2

    # Initialize a Jinja2 environment to render templates safely. By default autoescape is False, so we set it to True.
    env_jinja = jinja2.Environment(autoescape=True)

    # Step 4: Write the code - Render the template using Jinja2's `get_template` method and pass in the user-provided name parameter for rendering
    template = env["environment"]["templates"].get(
        "template"
    )  # Ensure 'template' is a valid, existing key in the environment dictionary
    rendered = env_jinja.from_string(template).render(name=name)

    # Return an HTTP response with the rendered template content
    return {"response": rendered}


def home(env):
    # Call `render_response_from_env` and store its return value as the response for this request
    response = render_response_from_env(env)

    # Return the generated response
    return response


# Example usage:
home_example = {
    "request": {"name": "example_template"},
    "environment": {"templates": {"template": "<p>{{ name | safe }}</p>"}},
}

print(home(home_example)["response"])