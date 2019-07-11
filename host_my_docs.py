
import requests
import base64


class HostMyDocs:

    def __init__(self, host: str='localhost', port: int=5000):
        self._base_url = 'http://{}:{}'.format(host, port)

    def add_project(self, name: str, description: str, logo: str=None):
        data = {
            'name': name,
            'description': description,
        }

        if logo is not None:
            data['logo'] = logo

        url = self._base_url + '/hmfd/projects'
        response = requests.post(url, json=data)
        if response.status_code != 200:
            raise RuntimeError('Error during adding project ' + name)

    def get_projects(self) -> dict:
        url = self._base_url + '/hmfd/projects'
        response = requests.get(url)
        if response.status_code != 200:
            raise RuntimeError('Error during getting projects')

        return response.json()

    def update_project_description(self, project: str, description: str):
        url = self._base_url + '/hmfd/projects/{}/description'.format(project)

        data = {'description': description}

        response = requests.patch(url, json=data)
        if response.status_code != 200:
            raise RuntimeError('Error during updating project description')

    def update_project_logo(self, project: str, logo: str):
        url = self._base_url + '/hmfd/projects/{}/logo'.format(project)

        data = {'logo': logo}

        response = requests.patch(url, json=data)
        if response.status_code != 200:
            raise RuntimeError('Error during updating project logo')

    def add_doc_files(self, project: str, version: str, filename: str):
        url = self._base_url + '/hmfd/projects/{}/{}/file'.format(project, version)

        response = requests.post(url, files={'file': open(filename, 'rb')})
        if response.status_code != 200:
            raise RuntimeError('Error during uploading new doc version')

    def add_doc_url(self, project: str, version: str, link: str):
        url = self._base_url + '/hmfd/projects/{}/{}/link'.format(project, version)

        data = {'url': link}
        response = requests.post(url, json=data)
        if response.status_code != 200:
            raise RuntimeError('Error during uploading new doc version')

    @staticmethod
    def logo_from_file(filename: str) -> str:
        with open(filename, 'rb') as f:
            data = f.read()

        return 'data:image/png;base64,' + base64.b64encode(data).decode('utf8')


if __name__ == "__main__":

    client = HostMyDocs()

    projects = client.get_projects()
    print(projects)
