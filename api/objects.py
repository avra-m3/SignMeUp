import re
import tempfile
import uuid

from flask import current_app as app
from flask import Response, jsonify
from flask import request as inbound
from flask_api import status
from google.cloud import storage
from peewee import DoesNotExist
from playhouse.shortcuts import model_to_dict

from core import process
from model.registration import Registration
from utilities import barcodes
from utilities.exception_router import NotAcceptable, NotFound, PreconditionFailed


def index():
    """
    GET the current server status.
    :return: Online - 200 OK
    """
    return Response("Online", status.HTTP_200_OK)


def register(club_name):
    """
    PUT a registration into the system
    :param club_name: The club name the registration should be tied to
    :return: The Request object tracking the status of the new registration
    :raises NotAcceptable: When the file given does not exist/ or is invalid
    """

    # Confirm the form data includes a key for 'student_card'
    if 'student_card' not in inbound.files:
        raise NotAcceptable("No student_card file parameter was parsed as part of the request.")
    upload = inbound.files['student_card']

    # Check the file is not empty (This is caused by the browser)
    if upload.filename == '':
        raise NotAcceptable("The file passed had no file name")

    # Make a temporary file and write the upload to it.
    temp = tempfile.NamedTemporaryFile()
    temp.close()

    upload.save(temp.name)

    # Pass the file path to the barcode processor for processing.
    card_number = barcodes.process(temp.name)
    match = re.match("^21259(\d{7})\d{2}$", card_number)
    if match is None:
        raise PreconditionFailed("Could not detect a valid barcode in the image provided")

    user_id = match.groups()[0]
    try:
        reg = Registration.get(club=club_name, student=user_id)
    except DoesNotExist:
        # Upload the file
        image_location = create(card_number, club_name, temp.name)
        reg = process(image_location, user_id, club_name)

    # Return a copy of the new request object in the database.
    return jsonify(model_to_dict(reg))


def get_registration(registration_id):
    """
    GET the details of an existing registration
    :param registration_id:
    :return: A JSON/Flask response containing the Registration object.
    :raises NotFound: if a registration matching the above does not exist
    """
    try:
        # TODO: Reconsider what we should be returning.
        reg = Registration.get_by_id(registration_id)
        return jsonify(model_to_dict(reg, recurse=True))

    except DoesNotExist:
        raise NotFound("A registration was not found matching the information given")


def store(path: str, name: str):
    """
    Store path into the remote Storage with an object id of name
    :param path: The path to the file to upload
    :param name: The name to give the file in the database.
    :return: The url/location of the object
    """
    client = storage.Client()
    # TODO: Change the bucket id to an app.config variable.
    bucket = client.get_bucket(app.config["GCLOUD_BUCKET"])
    upload = bucket.blob(name)
    upload.upload_from_filename(path)
    return upload.public_url


def create(card_number, club_name, path):
    """
    Uploads the image to Storage and Creates the object into the database
    :param card_number: The barcode id of the card
    :param club_name: The club to register too
    :param path: The path to the local copy of the card.
    :return: Reference to the Request model for the newly created request.
    :raises Upstream errors from the google.storage library
    """
    return store(path, "request_{}_{}_{}.png".format(card_number, club_name, uuid.uuid4()))
