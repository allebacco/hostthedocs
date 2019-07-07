import os

from flask import abort, Flask, jsonify, redirect, render_template, request

from . import getconfig, util
from .filekeeper import delete_files, insert_link_to_latest, parse_docfiles, unpack_project
from . import database

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


@app.route('/hmfd', methods=['POST'])
def add_documentation():
    if getconfig.readonly:
        return abort(403)

    if not request.files:
        return abort(400, 'Request is missing a zip file.')
    uploaded_file = util.UploadedFile.from_request(request)
    unpack_project(
        uploaded_file,
        request.form,
        getconfig.docfiles_dir
    )
    uploaded_file.close()

    return jsonify({'success': True})


@app.route('/hmfd', methods=['DELETE'])
def delete_documentation():
    if getconfig.readonly:
        return abort(403)

    if getconfig.disable_delete:
        return abort(403)

    delete_files(
        request.args['name'],
        request.args.get('version'),
        getconfig.docfiles_dir,
        request.args.get('entire_project')
    )

    return jsonify({'success': True})


@app.route('/')
def home():
    projects = parse_docfiles(getconfig.docfiles_dir, getconfig.docfiles_link_root)
    insert_link_to_latest(projects, '%(project)s/latest')
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
