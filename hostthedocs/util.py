"""
Provides utility methods.
"""

import os
import logging


logger = logging.getLogger()


class UploadedFile(object):
    """
    UploadedFile represents a file uploaded during a POST request.
    """

    def __init__(self, file_):
        """Instantiate an UploadedFile
        """
        self._file = file_

    @classmethod
    def from_request(cls, request):
        """
        Instantiate an UploadedFile from the first file in a request.

        :param werkzeug.wrappers.BaseRequest request: The POST request.
        :return: The instantiated UploadedFile.
        :raises ValueError: if no files exist within the request.
        """
        uploaded_files = list(request.files.values())
        if len(uploaded_files) > 1:
            logger.warning(
                'Only one file can be uploaded for each request. '
                'Only the first file will be used.'
            )
        elif len(uploaded_files) == 0:
            raise ValueError('Request does not contain uploaded file')

        current_file = uploaded_files[0]
        return cls(current_file)

    def get_filename(self):
        return self._file.filename

    def get_stream(self):
        return self._file.stream

    def save(self, directory):
        filename = os.path.join(directory, self.get_filename())
        self._file.save(filename)
        return filename

    def close(self):
        """close the file stream
        """
        try:
            self.get_stream().close()
        except:
            pass
