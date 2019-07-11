import os

from flask import abort, Flask, jsonify, redirect, render_template, request

from .util import UploadedFile
from .entities import Version
from . import getconfig, util
from .filekeeper import delete_files, insert_link_to_latest, parse_docfiles, unpack_project
from . import database, documents

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = getconfig.max_content_mb * 1024 * 1024


@app.route('/api/v1/projects', methods=['POST'])
def add_project():
    if getconfig.readonly:
        return abort(403)

    json_data = request.get_json()
    if json_data is None:
        abort(400, "Missing or invalid JSON data")
    if 'name' not in json_data:
        abort(400, "name missing from JSON data")
    if 'description' not in json_data:
        abort(400, "description missing from JSON data")

    if 'logo' in json_data:
        logo = json_data['logo']
    else:
        logo = 'http://placehold.it/96x96'

    ok = database.add_project(json_data['name'], json_data['description'], logo)

    if ok:
        return jsonify({'success': True})

    return abort(500)


@app.route('/api/v1/projects', methods=['GET'])
def get_projects():

    projects = database.get_projects()
    return jsonify([p.to_dict() for p in projects])


@app.route('/api/v1/projects/<project_name>', methods=['GET'])
def get_project(project_name):

    project = database.get_project(project_name)
    return jsonify(project.to_dict())


@app.route('/api/v1/projects/<project>/description', methods=['PATCH'])
def update_project_description(project):
    if getconfig.readonly:
        return abort(403)

    json_data = request.get_json()
    if json_data is None:
        abort(400, "Missing or invalid JSON data")
    if 'description' not in json_data:
        abort(400, "description missing from JSON data")

    ok = database.update_project_description(project, json_data['description'])

    if ok:
        return jsonify({'success': True})

    return abort(500)


@app.route('/api/v1/projects/<project>/logo', methods=['PATCH'])
def update_project_logo(project):
    if getconfig.readonly:
        return abort(403)

    json_data = request.get_json()
    if json_data is None:
        abort(400, "Missing or invalid JSON data")
    if 'logo' not in json_data:
        abort(400, "logo missing from JSON data")

    ok = database.update_project_logo(project, json_data['logo'])

    if ok:
        return jsonify({'success': True})

    return abort(500)


@app.route('/api/v1/projects/<project>/<version>/file', methods=['POST'])
def add_doc_files(project, version):
    if getconfig.readonly:
        return abort(403)

    if not request.files:
        return abort(400, 'Request is missing a zip file.')

    uploaded_file = UploadedFile.from_request(request)
    ok = documents.add_document(project, version, uploaded_file)
    if not ok:
        return abort(500, 'Error during processing request')

    return jsonify({'success': True})


@app.route('/api/v1/projects/<project>/<version>/link', methods=['POST'])
def add_doc_link(project, version):
    if getconfig.readonly:
        return abort(403)

    print('Add link for ', project, 'to', version)

    json_data = request.get_json()
    if json_data is None:
        abort(400, "Missing or invalid JSON data")
    if 'url' not in json_data:
        abort(400, "url missing from JSON data")

    url = json_data['url']
    ok = database.add_version(project, Version(version, url))
    if not ok:
        return abort(500, 'Error during processing request')

    return jsonify({'success': True})


@app.route('/')
def home():
    projects = database.get_projects()
    return render_template('index.html', projects=projects, **getconfig.renderables)


@app.route('/<project_name>/latest/')
def latest_root(project_name):
    return latest(project_name, '')


@app.route('/<project_name>/latest/<path:path>')
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
