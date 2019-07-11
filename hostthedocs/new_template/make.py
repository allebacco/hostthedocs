import os
import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

BASE_DIR = '/home/crash/Desktop/Progetti/Zero/app/theme/docs'
JINJA_DEST = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'index.html')
CONF_FILE = 'conf.yml'


def make_jinja_env():
    return Environment(
        loader=FileSystemLoader(os.path.dirname(os.path.realpath(__file__))),
        undefined=StrictUndefined # raise exception if key is not provided
    )

def render_template(template, env):
    jinja_template = env.get_template('index.j2')
    rendered_template = jinja_template.render(template)

    if not os.path.exists(os.path.dirname(JINJA_DEST)):
        os.makedirs(os.path.dirname(JINJA_DEST))
    with open(JINJA_DEST, "w") as fh:
        fh.write(rendered_template)


def parse_metadata(project_metadata):
    try:
        metadata = yaml.safe_load(project_metadata)
        metadata['latest'] = metadata['versions'][0]
        if len(metadata['versions']) > 1:
            metadata['previous'] = metadata['versions'][1:]
        else:
            metadata['previous'] = list()

        return metadata
    except yaml.YAMLError as exc:
        print(exc)


if __name__ == '__main__':
    template = dict()
    template['project_metadata'] = list()
    projects = next(os.walk(BASE_DIR))[1]
    for project in projects:
        with open(os.path.join(BASE_DIR, project, CONF_FILE), 'r') as project_metadata:
            template['project_metadata'].append(parse_metadata(project_metadata))

    print(template)
    render_template(template, make_jinja_env())
