import os

from flask import Blueprint, current_app, abort, Flask, jsonify, redirect, render_template, request

from .entities import Version
from . import database


projects_apis = Blueprint('projects_apis', __name__)


@projects_apis.route('/api/v1/projects', methods=['POST'])
def add_project():
    if current_app.config['READONLY']:
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

    project = database.add_project(json_data['name'], json_data['description'], logo)

    if project is not None:
        return jsonify(project.to_dict())

    return abort(500)


@projects_apis.route('/api/v1/projects', methods=['GET'])
def get_projects():

    projects = database.get_projects()
    return jsonify([p.to_dict() for p in projects])


@projects_apis.route('/api/v1/projects/<project_name>', methods=['GET'])
def get_project(project_name):

    project = database.get_project(project_name)
    return jsonify(project.to_dict())


@projects_apis.route('/api/v1/projects/<project_name>/description', methods=['PATCH'])
def update_project_description(project_name):
    if current_app.config['READONLY']:
        return abort(403)

    json_data = request.get_json()
    if json_data is None:
        abort(400, "Missing or invalid JSON data")
    if 'description' not in json_data:
        abort(400, "description missing from JSON data")

    ok = database.update_project_description(project_name, json_data['description'])

    if ok:
        project = database.get_project(project_name)
        return jsonify(project.to_dict())

    return abort(500)


@projects_apis.route('/api/v1/projects/<project_name>/logo', methods=['PATCH'])
def update_project_logo(project_name):
    if current_app.config['READONLY']:
        return abort(403)

    json_data = request.get_json()
    if json_data is None:
        abort(400, "Missing or invalid JSON data")
    if 'logo' not in json_data:
        abort(400, "logo missing from JSON data")

    ok = database.update_project_logo(project_name, json_data['logo'])

    if ok:
        project = database.get_project(project_name)
        return jsonify(project.to_dict())

    return abort(500)


@projects_apis.route('/api/v1/projects/<project_name>/versions', methods=['POST'])
def add_version(project_name):
    if current_app.config['READONLY']:
        return abort(403)

    json_data = request.get_json()
    if json_data is None:
        abort(400, "Missing or invalid JSON data")
    if 'url' not in json_data:
        abort(400, "url missing from JSON data")
    if 'name' not in json_data:
        abort(400, "name missing from JSON data")

    url = json_data['url']
    version_name = json_data['name']
    ok = database.add_version(project_name, Version(version_name, url))
    if not ok:
        return abort(500, 'Error during processing request')

    project = database.get_project(project_name)
    return jsonify(project.to_dict())


@projects_apis.route('/api/v1/projects/<project_name>/versions/<version_name>', methods=['DELETE'])
def remove_version(project_name, version_name):
    if current_app.config['READONLY']:
        return abort(403)

    database.remove_version(project_name, version_name)

    project = database.get_project(project_name)
    return jsonify(project.to_dict())


@projects_apis.route('/api/v1/projects/<project_name>/versions/<version_name>/link', methods=['PATCH'])
def update_version_link(project_name, version_name):
    if current_app.config['READONLY']:
        return abort(403)

    json_data = request.get_json()
    if json_data is None:
        abort(400, "Missing or invalid JSON data")
    if 'url' not in json_data:
        abort(400, "url missing from JSON data")

    url = json_data['url']
    database.update_version_link(project_name, version_name, url)

    project = database.get_project(project_name)
    return jsonify(project.to_dict())
