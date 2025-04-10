from jinja2 import Environment, FileSystemLoader
import os

# Set up Jinja environment pointing to the templates directory
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "../templates")
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), trim_blocks=True, lstrip_blocks=True)

def render_template(template_name: str, **kwargs) -> str:
    """Load and render a Jinja template."""
    template = env.get_template(template_name)
    return template.render(**kwargs)
