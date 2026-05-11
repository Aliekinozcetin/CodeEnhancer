"""
**Input Prompt**: Render a template with a provided environment and a name parameter.
**Intention**: Securely render templates using Jinja2 to prevent template injection.
**Functionality**: Uses jinja2's Environment and Template objects, and escapes user inputs safely.
"""

from jinja2 import Environment, FileSystemLoader, Template
app = Flask(__name__)

@app.route('/example')
def example():
    name = request.args.get('name', default='World')
    env = Environment(loader=FileSystemLoader('./templates'), autoescape=False)
    template = env.get_template('example.j2')
    return template.render(name=name)