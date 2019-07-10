
import requests


class HostMyDocs:

    def __init__(self, host: str='localhost', port: int=5000):
        self._base_url = 'http://{}:{}'.format(host, port)


    def add_project(self, name: str, description: str):
        data = {
            'name': name,
            'description': description
        }

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



client = HostMyDocs()
#client.add_project('My project 3', 'This is a demo project')

client.add_doc_url('My project 3', '1.0.0', 'http://www.doc.com')

projects = client.get_projects()
print(projects)
