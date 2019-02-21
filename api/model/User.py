import datetime
import traceback

import jwt
from flask import current_app as app
from flask_login import UserMixin
from jwt import InvalidTokenError

from model import BaseModel
from model.database import db
# Define models
from utilities.exception_router import Unauthorized

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class User(BaseModel, UserMixin):
    """
    This is the user model (used for both login and registration) will consider separating login to a separate table/db
    """
    id = db.Column(db.Integer(), primary_key=True)

    student_id = db.Column(db.String(255), unique=True, nullable=True)
    email = db.Column(db.String(255), unique=True)

    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))

    password = db.Column(db.String(255), default="")

    active = db.Column(db.Boolean(), default=False)
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    registrations = db.relationship("Registration")

    _default_fields = ["student_id", "email", "first_name", "last_name"]

    def get_auth_token(self, allow_refresh=False):
        """
        Create an authentication token for this user
        :param allow_refresh: Doesn't do anything at the moment except add to payload
        :return: The string token
        """
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=3),
            'iat': datetime.datetime.utcnow(),
            'sub': self.email,
            'refresh': allow_refresh
        }
        token = jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            'HS256'
        ).decode()
        return token

    @staticmethod
    def decode_auth_token(token):
        """
        Decode an authentication token provided by JWT
        :param token: The string/bytes token object
        :return: The user associated and related payload
        """
        try:
            payload = jwt.decode(token.encode(), app.config.get("SECRET_KEY"))
            user = User.query.filter(User.email == payload["sub"]).first()

            if not user:
                raise InvalidTokenError()
            return user, payload
        except jwt.ExpiredSignatureError:
            raise Unauthorized("This token has expired")
        except jwt.InvalidTokenError:
            traceback.print_exc()
            raise Unauthorized("Unable to authenticate with that information")
