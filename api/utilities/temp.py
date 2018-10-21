import os
import uuid
from typing import Any

from modules.path_constants import PATHS
from utilities.exception_router import BadRequest


class TempFile:
    directory: str
    name: str
    ext: str
    file: Any

    def __init__(self, directory, file):
        self.directory = directory
        self.name = uuid.uuid4()
        self.ext = file.filename.rsplit(".", 1)[-1].lower()
        self.file = file

    @property
    def path(self):
        return os.path.join(self.directory, "{}.{}".format(self.name, self.ext))

    def __enter__(self):
        if self.ext not in PATHS.IMAGE_FORMATS:
            raise BadRequest(
                "Image format was not in set of allowed formats {}.".format(", ".join(PATHS.IMAGE_FORMATS)))
        self.file.save(self.path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.remove(self.path)
