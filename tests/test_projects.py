from listthedocs import ListTheDocs

import pytest


def test_add_project_creates_and_returns_the_project(client):

    response = client.post('/api/v1/projects', json={'name': 'test_project', 'description': 'A very long string'})
    assert response.status_code == 200

    project = response.get_json()
    assert 'name' in project
    assert project['name'] == 'test_project'
    assert 'description' in project
    assert project['description'] == 'A very long string'
    assert 'logo' in project


def test_get_project_returns_the_project(client):

    response = client.post('/api/v1/projects', json={'name': 'test_project', 'description': 'A very long string'})
    assert response.status_code == 200

    response = client.get('/api/v1/projects/test_project')
    assert response.status_code == 200

    project = response.get_json()
    assert 'name' in project
    assert project['name'] == 'test_project'
    assert 'description' in project
    assert project['description'] == 'A very long string'
    assert 'logo' in project


def test_get_projects_returns_all_the_projects(client):

    response = client.post('/api/v1/projects', json={'name': 'test_project_1', 'description': 'Tests description 1'})
    assert response.status_code == 200

    response = client.post('/api/v1/projects', json={'name': 'test_project_2', 'description': 'Tests description 2'})
    assert response.status_code == 200

    response = client.get('/api/v1/projects')
    assert response.status_code == 200

    projects = response.get_json()
    assert isinstance(projects, list)
    assert projects[0]['name'] == 'test_project_1'
    assert projects[0]['description'] == 'Tests description 1'
    assert projects[1]['name'] == 'test_project_2'
    assert projects[1]['description'] == 'Tests description 2'


def test_update_project_description(client):

    response = client.post('/api/v1/projects', json={'name': 'test_project', 'description': 'A very long string'})
    assert response.status_code == 200

    response = client.patch('/api/v1/projects/test_project/description', json={'description': 'Short string'})
    assert response.status_code == 200

    project = response.get_json()
    assert 'name' in project
    assert project['name'] == 'test_project'
    assert 'description' in project
    assert project['description'] == 'Short string'
    assert 'logo' in project


def test_update_project_logo(client):

    response = client.post('/api/v1/projects', json={'name': 'test_project', 'description': 'A very long string'})
    assert response.status_code == 200

    response = client.patch('/api/v1/projects/test_project/logo', json={'logo': 'image.jpg'})
    assert response.status_code == 200

    project = response.get_json()
    assert 'name' in project
    assert project['name'] == 'test_project'
    assert 'description' in project
    assert project['description'] == 'A very long string'
    assert 'logo' in project
    assert project['logo'] == 'image.jpg'


def test_add_version(client):

    response = client.post('/api/v1/projects', json={'name': 'test_project', 'description': 'A very long string'})
    assert response.status_code == 200

    response = client.post('/api/v1/projects/test_project/1.0.0/link', json={'url': 'www.example.com/index.html'})
    assert response.status_code == 200

    project = response.get_json()
    assert 'name' in project
    assert project['name'] == 'test_project'
    assert 'description' in project
    assert project['description'] == 'A very long string'
    assert 'logo' in project
    assert 'versions' in project
    assert isinstance(project['versions'], list)
    assert project['versions'][0]['version'] == '1.0.0'
    assert project['versions'][0]['url'] == 'www.example.com/index.html'
