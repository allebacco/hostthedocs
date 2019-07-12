

import os

from flask import abort, redirect, render_template, Blueprint

from . import getconfig
from . import database


webui = Blueprint('webui', __name__, template_folder='templates')


@webui.route('/')
def home():
    projects = database.get_projects()
    return render_template('index.html', projects=projects, **getconfig.renderables)


@webui.route('/<project_name>/latest/')
def latest_root(project_name):
    return latest(project_name, '')


@webui.route('/<project_name>/latest/<path:path>')
def latest(project_name, path):
    project = database.get_project(project_name)

    if project is None:
        abort(404)

    latest_version = project.get_latest_version()
    if latest_version is None:
        abort(404)

    latestindex = latest_version.url
    if path:
        # Remove 'index.html' for doc url
        if latestindex.endswith('index.html'):
            latestindex = latestindex[:-len('/index.html')]
        latestlink = '%s/%s' % (latestindex, path)
    else:
        latestlink = latestindex

    return redirect(latestlink)
