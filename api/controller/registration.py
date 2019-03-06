from flask import jsonify

from model import Registration, User, Club
from model.database import db
from modules.ocr import attempt_recognition
from modules.ocr.request import request_oct_from_image
from utilities.database import insert_new_registration
from utilities.exception_router import NotFound, BadRequest
from utilities.file_handling import safely_accept_file
from utilities.security import require_auth_token


@require_auth_token
def list(club_name):
    """
    GET /club/<club_name>/register
    :param club_name:
    :return:
    """
    registrations = Registration.query.join(User, User.id == Registration.user_id).join(
        Club, Club.id == Registration.club_id).filter(Club.abbreviation == club_name).all()
    return jsonify([registration.to_dict() for registration in registrations])


@require_auth_token
def get(club_name, student_id):
    """
    GET /club/<club_name>/register/<student_id>
    :param club_name:
    :param student_id:
    :return:
    """
    registration = Registration.query.join(User, User.id == Registration.user_id).join(
        Club, Club.id == Registration.club_id).filter(
        User.student_id == student_id, Club.abbreviation == club_name).first()
    if not registration:
        raise NotFound("A registration was not found matching the information given")
    return jsonify(registration.to_dict())


@require_auth_token
def create(club_name):
    """
    PUT a registration into the system
    :param club_name: The club name the registration should be tied to
    :return: The Request object tracking the status of the new registration
    :raises NotAcceptable: When the file given does not exist/ or is invalid
    """

    if not Club.query.filter(Club.abbreviation == club_name).first():
        raise BadRequest("Could not locate the requested club ({})".format(club_name))

    uploaded_file = safely_accept_file()

    user, card = attempt_recognition(path=uploaded_file, provider=request_oct_from_image)

    registration = insert_new_registration(user.source, club_name, card.expiry)

    return jsonify(registration.to_dict())
