import traceback

from model import Club
from model import User, Registration
from model.database import db
from processor.modules.ocr.process import get_card_data
from processor.modules.ocr.request import request_ocr
from utilities.exception_router import APIException, BadRequest


def handle_processing_errors(fn):
    """
    Wrap process with error handling to ensure the model is put in an erred
    state when an exception occurs
    :param fn: The function to wrap
    :return: the wrapped function
    :raises None: This function suppresses ALL exceptions
    """

    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except APIException as ex:
            print("Exception occurred while processing - {}".format(repr(ex)))
            traceback.print_exc()
            raise
        except Exception as ex:
            print("Unexpected Exception occurred while processing - {}".format(repr(ex)))
            traceback.print_exc()
            raise APIException()

    return wrapper


@handle_processing_errors
def link_card(path_to_card: str, club_name: str):
    data = request_ocr(path_to_card)
    result = get_card_data(data)

    user = User.query.filter_by(student_id=result["user"]["student_id"]).first()
    club = Club.query.filter_by(abbreviation=club_name).first()

    if not user:
        user = User(**result["user"])
        db.session.add(user)
    if not club:
        club = Club(name=club_name)
        db.session.add(club)

    db.session.commit()
    registration = Registration.query.filter_by(user_id=user.id, club_id=club.id).first()

    if registration:
        raise BadRequest("Registration Already Exists")

    registration = Registration(user_id=user.id, club_id=club.id, evidence=path_to_card,
                                expiry=result["card"]["expiry"])
    db.session.add(registration)
    db.session.commit()
    return registration
