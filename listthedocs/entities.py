import natsort


class Version:

    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url

    @staticmethod
    def sort_by_version(version: 'Version'):
        # See http://natsort.readthedocs.io/en/stable/examples.html
        return version.name.replace('.', '~') + 'z'

    def to_dict(self):
        return {
            "name": self.name,
            "url": self.url
        }

    def copy(self):
        return Version(self.name, self.url)


class Project:

    def __init__(self, rowid: int, name: str, description: str, logo: str):
        self.rowid = rowid
        self.name = name
        self.description = description
        self.versions = list()
        self.logo = logo

    def add_versions(self, versions: 'Iterable[Version]'):
        self.versions = natsort.natsorted(versions, key=Version.sort_by_version)

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
