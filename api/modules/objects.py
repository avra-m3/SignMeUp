import os
import shutil

from flask import Response, request, jsonify
from flask_api import status

from modules.path_constants import PATHS
from modules.recognition import barcodes
from utilities.exception_router import NotAcceptable, Conflict
from utilities.temp import TempFile


def index():
    return Response("Hello World", status.HTTP_200_OK)


def register(club_name):
    if 'student_card' not in request.files:
        raise NotAcceptable("No student_card file parameter was parsed as part of the request.")
    file = request.files['student_card']

    if file.filename == '':
        raise NotAcceptable("The file passed had no file name")

    with TempFile(PATHS.TEMP, file) as temp:
        upload_id = barcodes.process(temp.path)
        new_fpath = os.path.join(PATHS.QUEUED, "{}_{}.{}".format(club_name, upload_id, temp.ext))
        if os.path.exists(new_fpath):
            raise Conflict("A student card with that ID has already been submitted for processing")
        registration = Provider().club(club_name).register(upload_id)
        shutil.copy(temp.path, new_fpath)

    return jsonify(registration.json)


def get_file_status(club_name, card_id):
    provider = Provider()
    return jsonify(provider.club(club_name).get_registration(card_id).json)
