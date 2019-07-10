import os
import zipfile

from .util import UploadedFile
from . import getconfig
from . import database
from .entities import Version


def _remove_failed_upload(version_dir: str, store_filename: str):
    if os.path.exists(version_dir):
        os.rmdir(version_dir)

    if os.path.exists(store_filename):
        os.remove(store_filename)


def add_document(project: str, version: str, uploaded_file: UploadedFile):

    project_dir = os.path.join(getconfig.docfiles_dir, project)
    version_dir = os.path.join(project_dir, version)

    # Store a copy of the compressed documentation
    store_filename = os.path.join(project_dir, version + '.zip')
    uploaded_file.save(store_filename)

    if not os.path.isdir(version_dir):
        os.makedirs(version_dir)

    # Expand documentation
    compressed_file = zipfile.ZipFile(store_filename)
    compressed_file.extractall(version_dir)

    if not os.path.exists(os.path.join(version_dir, 'index.html')):
        _remove_failed_upload(version_dir, store_filename)
        return False

    url = '%s/%s/%s/index.html' % (getconfig.docfiles_link_root, project, version)

    # Save version in database
    ok = database.add_version(project, Version(version, url))
    if not ok:
        _remove_failed_upload(version_dir, store_filename)
    
    return ok

