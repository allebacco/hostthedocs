from listthedocs import ListTheDocs

import pytest


def test_add_project_creates_the_project(client):

    response = client.post('/api/v1/projects', json={'name': 'test_project', 'description': 'A very long string'})
    assert response.status_code == 200

    response = client.get('/api/v1/projects/test_project')
    assert response.status_code == 200

    project = response.get_json()
    assert 'name' in project
    assert project['name'] == 'test_project'
    assert 'description' in project
    assert project['description'] == 'A very long string'
