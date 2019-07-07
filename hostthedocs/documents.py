import os
import zipfile

from . import getconfig
from . import database
from .entities import Version


def add_document(project: str, version: str, filename: str):

    project_dir = os.path.join(getconfig.docfiles_dir, project)
    version_dir = os.path.join(project_dir, version)

    if not os.path.isdir(version_dir):
        os.makedirs(version_dir)

    compressed_file = zipfile.ZipFile(filename)
    compressed_file.extractall(version_dir)

    url = '%s/%s/%s/index.html' % (getconfig.docfiles_link_root, project, version)

    return database.add_version(project, Version(version, url))

