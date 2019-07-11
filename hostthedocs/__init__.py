import os

from flask import abort, Flask, jsonify, redirect, render_template, request

from .util import UploadedFile
from .entities import Version
from . import getconfig, util
from .filekeeper import delete_files, insert_link_to_latest, parse_docfiles, unpack_project
from . import database, documents

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = getconfig.max_content_mb * 1024 * 1024


@app.route('/hmfd/projects', methods=['POST'])
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

    ok = database.add_project(json_data['name'], json_data['description'])

    if ok:
        return jsonify({'success': True})

    return abort(500)


@app.route('/hmfd/projects', methods=['GET'])
def get_projects():

    projects = database.get_projects()
    return jsonify([p.to_dict() for p in projects])


@app.route('/hmfd/projects/<project>/<version>/file', methods=['POST'])
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


@app.route('/hmfd/projects/<project>/<version>/link', methods=['POST'])
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


@app.route('/<project>/latest/')
def latest_root(project):
    return latest(project, '')


@app.route('/<project>/latest/<path:path>')
def latest(project, path):
    parsed_docfiles = parse_docfiles(getconfig.docfiles_dir, getconfig.docfiles_link_root)
    proj_for_name = dict((p['name'], p) for p in parsed_docfiles)
    if project not in proj_for_name:
        return 'Project %s not found' % project, 404

    if len(proj_for_name[project]['versions']) == 0:
        abort(404)

    latestindex = proj_for_name[project]['versions'][-1]['link']
    if path:
        latestlink = '%s/%s' % (os.path.dirname(latestindex), path)
    else:
        latestlink = latestindex
    # Should it be a 302 or something else?
    return redirect(latestlink)
