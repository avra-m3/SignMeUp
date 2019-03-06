from datetime import datetime

from model import Club, User, Registration
from model.database import db
from utilities.exception_router import BadRequest


def insert_new_registration(user_source, club_name, card_expiry):
    user = User.query.filter_by(student_id=user_source["student_id"]).first()
    club = Club.query.filter_by(abbreviation=club_name).first()

    if not user:
        user = User(**user_source)
        db.session.add(user)
    if not club:
        raise BadRequest("Registering to a non-existent club")
        # club = Club(name=club_name)
        # db.session.add(club)

    db.session.commit()
    registration = Registration.query.filter_by(user_id=user.id, club_id=club.id).first()

    if registration:
        raise BadRequest("Registration Already Exists")

    registration = Registration(user_id=user.id, club_id=club.id, evidence="Evidence temporarily disabled",
                                expiry=card_expiry)
    db.session.add(registration)
    db.session.commit()
    return registration
