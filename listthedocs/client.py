
import requests
import base64


class Version:

    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url

    def to_dict(self):
        return {
            "name": self.name,
            "url": self.url
        }

    @staticmethod
    def from_dict(obj: dict) -> 'Version':
        return Version(name=obj['name'], url=obj['url'])


class Project:

    def __init__(self, name: str, description: str, logo: str=None, versions=tuple()):
        self.name = name
        self.description = description
        self.versions = versions
        self.logo = logo

    def get_latest_version(self):
        if len(self.versions) == 0:
            return None

        return self.versions[-1]

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "versions": [v.to_dict() for v in self.versions],
            'logo': self.logo
        }

    @staticmethod
    def from_dict(obj: dict) -> 'Project':
        return Project(
            name=obj['name'], description=obj['description'],
            logo=obj['logo'],
            versions=tuple(Version.from_dict(v) for v in obj['versions']),
        )




class ListTheDocs:

    def __init__(self, host: str='localhost', port: int=5000):
        self._base_url = 'http://{}:{}'.format(host, port)
        self._session = requests.Session()

    def add_project(self, project: Project) -> Project:
        url = self._base_url + '/api/v1/projects'
        response = self._session.post(url, json=project.to_dict())
        if response.status_code != 200:
            raise RuntimeError('Error during adding project ' + project.name)

        return Project.from_dict(response.json())

    def get_projects(self) -> 'tuple[Project]':
        url = self._base_url + '/api/v1/projects'
        response = requests.get(url)
        if response.status_code != 200:
            raise RuntimeError('Error during getting projects')

        return tuple(Project.from_dict(p) for p in response.json())

    def get_project(self, name) -> Project:
        url = self._base_url + '/api/v1/projects/{}'.format(name)
        response = requests.get(url)
        if response.status_code == 404:
            return None
        if response.status_code != 200:
            raise RuntimeError('Error during getting project ' + name)

        return Project.from_dict(response.json())

    def update_project_description(self, project_name: str, description: str) -> Project:
        url = self._base_url + '/api/v1/projects/{}/description'.format(project_name)
        response = requests.patch(url, json={'description': description})
        if response.status_code != 200:
            raise RuntimeError('Error during updating project description')

        return Project.from_dict(response.json())

    def update_project_logo(self, project_name: str, logo: str) -> Project:
        url = self._base_url + '/api/v1/projects/{}/logo'.format(project_name)
        response = requests.patch(url, json={'logo': logo})
        if response.status_code != 200:
            raise RuntimeError('Error during updating project logo')

        return Project.from_dict(response.json())

    def add_version(self, project_name: str, version: Version) -> Project:
        url = self._base_url + '/api/v1/projects/{}/versions'.format(project_name)
        response = requests.post(url, json=version.to_dict())
        if response.status_code != 200:
            raise RuntimeError('Error during uploading new doc version')

        return Project.from_dict(response.json())

    def delete_version(self, project_name: str, version_name: str) -> Project:
        url = self._base_url + '/api/v1/projects/{}/versions/{}'.format(project_name, version_name)
        response = requests.delete(url)
        if response.status_code != 200:
            raise RuntimeError('Error during uploading new doc for version ' + version_name)

        return Project.from_dict(response.json())

    def update_version_url(self, project_name: str, version_name: str, new_url: str) -> Project:
        url = self._base_url + '/api/v1/projects/{}/versions/{}/link'.format(project_name, version_name)
        response = requests.patch(url, json={'url': new_url})
        if response.status_code != 200:
            raise RuntimeError('Error during uploading new url for version ' + version_name)

        return Project.from_dict(response.json())

    @staticmethod
    def load_logo_from_file(filename: str) -> str:
        with open(filename, 'rb') as f:
            data = f.read()

        return 'data:image/png;base64,' + base64.b64encode(data).decode('utf8')
