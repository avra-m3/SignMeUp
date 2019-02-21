import tempfile
import uuid

from flask import Response, jsonify
from flask import current_app as app
from flask import request as inbound
from flask_api import status
from flask_login import current_user
from flask_security import roles_accepted, SQLAlchemyUserDatastore, http_auth_required
from flask_security.utils import hash_password
from google.cloud import storage

from model import Registration, User, Club, Role, BaseModel
from model.database import db
from processor.core import link_card
from utilities.exception_router import NotAcceptable, NotFound, BadRequest, Forbidden
from utilities.security import require_auth_token


def index():
    """
    GET the current server status.
    :return: Online - 200 OK
    """
    return Response("Online", status.HTTP_200_OK)


@require_auth_token
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

    if not Club.query.filter(Club.abbreviation == club_name).first():
        raise BadRequest("Could not locate the requested club ({})".format(club_name))

    # Make a temporary file and write the upload to it.
    temp = tempfile.NamedTemporaryFile()
    temp.close()

    upload.save(temp.name)

    path_to_card = create(uuid.uuid4(), club_name, temp.name)

    registration = link_card(path_to_card, club_name)

    return jsonify(registration.to_dict())


@require_auth_token
def get_registration(registration_id):
    """
    GET the details of an existing registration
    :param registration_id:
    :return: A JSON/Flask response containing the Registration object.
    :raises NotFound: if a registration matching the above does not exist
    """
    registration = Registration.query.filter_by(id=registration_id).first()
    if not registration:
        raise NotFound("A registration was not found matching the information given")
    return jsonify(registration.to_dict())


@require_auth_token
def get_registration_by_details(student_id, club_name):
    """
    GET the details of an existing registration by the registration information
    :param student_id:
    :param club_name:
    :return: A JSON/Flask response containing the Registration object.
    :raises NotFound: if a registration matching the above does not exist
    """
    registration = Registration.query.join(User, User.id == Registration.user_id).join(
        Club, Club.id == Registration.club_id).filter(
        User.student_id == student_id, Club.abbreviation == club_name).first()
    if not registration:
        raise NotFound("A registration was not found matching the information given")
    return jsonify(registration.to_dict())


@require_auth_token
def update_user_by_student_id(student_id, first_name, last_name, email):
    """
    UPDATE the details of an existing user by the student_id
    :param email: new email
    :param last_name: new last name
    :param first_name: new first name
    :param student_id: new student id
    :return: A JSON/Flask response containing the Registration object.
    :raises NotFound: if a registration matching the above does not exist
    """
    user = User.query.filter(User.student_id == student_id).first()

    user.first_name = first_name
    user.last_name = last_name
    user.email = email

    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict())


@require_auth_token
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


@require_auth_token
@roles_accepted("admin")
def create_user(email: str, password: str):
    datastore = SQLAlchemyUserDatastore(db, User, Role)

    if not datastore.get_user(email):
        datastore.create_user(email=email, password=hash_password(password))
        db.session.commit()

        return jsonify(User.query.filter(User.email == email).first().to_dict())
    return jsonify(User.query.filter(User.email == email).first().to_dict())


@require_auth_token
def get_user(email):
    user = User.query.filter(User.email == email).first()
    if not user:
        raise NotFound("A user with that email address did not exist")
    return jsonify(user.to_dict())


@require_auth_token
def get_clubs():
    return jsonify({
        "data": [BaseModel.to_dict(club) for club in Club.query.all()]
    })


@http_auth_required
def authorize():
    """
    Generate an authorization token from a username/password
    :return:
    """
    if current_user.active:
        return jsonify({
            "email": current_user.email,
            "active": current_user.active,
            "token": current_user.get_auth_token(),
        })
    raise Forbidden("Account has been deactivated")


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
