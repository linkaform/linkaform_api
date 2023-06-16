# coding: utf-8

from jinja2 import Environment, FileSystemLoader
import json



def read_template_file(file_path, file_name, file_data=None):
    # Create a Jinja2 environment
    env = Environment(loader=FileSystemLoader(f'{file_path}'))
    # Load the template
    template = env.get_template(file_name)
    # Load and parse the JSON data
    cr, data = get_cr_data()
    model_data = get_cr_data
    user_data = json.loads(json_data)
    # Render the template with JSON data
    output = template.render(model_data, file_data=file_data)

    # Print or use the rendered output
    print(output)
