import os
import shutil
import uuid

from flask import Response, request, jsonify
from flask_api import status

from modules.image_processing import barcodes
from utilities.exception_router import NotAcceptable, BadRequest, Conflict

IMAGE_FORMATS = ["png", "jpg", "jpeg", "gif"]


class PATHS:
    ROOT = "./processing"
    TEMP = "{}/uploaded".format(ROOT)
    QUEUED = "{}/queue".format(ROOT)
    DONE = "{}/complete".format(ROOT)

    @staticmethod
    def create_dirs():
        if not os.path.exists(PATHS.ROOT):
            os.mkdir(PATHS.ROOT)
        if not os.path.exists(PATHS.TEMP):
            os.mkdir(PATHS.TEMP)
        if not os.path.exists(PATHS.QUEUED):
            os.mkdir(PATHS.QUEUED)
        if not os.path.exists(PATHS.DONE):
            os.mkdir(PATHS.DONE)


def index():
    return Response("Hello World", status.HTTP_200_OK)


def register():
    if 'student_card' not in request.files:
        raise NotAcceptable("No student_card file parameter was parsed as part of the request.")
    file = request.files['student_card']
    if file.filename == '':
        raise NotAcceptable("The file passed had no file name")

    file_type = file.filename.rsplit(".", 1)[-1].lower()
    if file_type not in IMAGE_FORMATS:
        raise BadRequest("Image format was not in set of allowed formats {}.".format(", ".join(IMAGE_FORMATS)))
    fpath = os.path.join(PATHS.TEMP, str(uuid.uuid4()) + "." + file_type)
    file.save(fpath)

    upload_id = barcodes.process(fpath)
    new_fpath = os.path.join(PATHS.QUEUED, upload_id + "." + file_type)

    if os.path.exists(new_fpath):
        os.remove(fpath)
        raise Conflict("A student card with that ID has already been submitted for processing")

    shutil.copy(fpath, new_fpath)
    os.remove(fpath)

    return jsonify({
        "code": 200,
        "status": "HTTP Status 200 OK",
        "message": "File successfully queued for processing",
        "file": {
            "id": upload_id,
            "status": "queued",
        }
    })
