import tempfile
import uuid
from datetime import datetime

from flask import Response, jsonify
from flask import request as inbound
from flask_api import status
from google.cloud import storage
from peewee import DoesNotExist
from playhouse.shortcuts import model_to_dict

from model import base
from model.registration import Registration
from model.request import Request as RequestModel
from utilities import barcodes
from utilities.exception_router import NotAcceptable, Conflict, NotFound


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
    temp.write(upload.read())
    temp.close()

    # Pass the file path to the barcode processor for processing.
    card_number = barcodes.process(temp.name)

    # Upload the file and create entries into the database
    request = create(card_number, club_name, temp.name)

    # Return a copy of the new request object in the database.
    return jsonify(model_to_dict(request))


def get_file_status(club_name, request_id):
    """
    GET the status of a request
    :param club_name: The club the request was made to
    :param request_id: The ID of the request.
    :return: A JSON/FLASK response containing the Request Object
    :raises NotFound: When no request matching the ID given exists.
    :raises Conflict: When the request exists but is not linked to the club_name given.
    """
    try:
        request = RequestModel.get_by_id(request_id)

        if request.club != club_name:
            raise Conflict("The club given did not match the registration id")

        return jsonify(model_to_dict(request))
    except DoesNotExist:
        raise NotFound("That request does not exist.")


def get_registration(club_name, user_id, year=datetime.now().year):
    """
    GET the details of an existing registration
    :param club_name: The name of the club to check
    :param year: The year to check
    :param user_id: The user id to get details for.
    :return: A JSON/Flask response containing the Registration object.
    :raises NotFound: if a registration matching the above does not exist
    """
    try:
        # TODO: Reconsider what we should be returning.
        reg = Registration.get(club_id=club_name, card_id=user_id, year=year)
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
    bucket = client.get_bucket("csit-cache")
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
    with base.database.atomic() as tx:
        try:
            request = RequestModel.create(card_number=card_number, club_name=club_name, url="")

            destination = store(path, "request_{}_{}.png".format(request.id, uuid.uuid4()))

            request.image_location = destination
            request.save()
            return request
        except Exception:
            # Rollback the create if the image could not be uploaded into storage
            tx.rollback()
            raise
