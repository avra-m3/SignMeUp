from flask import request
from flask_security import Security, SQLAlchemyUserDatastore, login_user
from flask_security.utils import hash_password

from model import Role
from model import User
from model.database import db
from utilities.exception_router import Unauthorized

security = Security()


def setup(app):
    """
    Setup Flask Security
    :param app: The Flask Application Object
    :return: None
    """
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore)

    if app.config["DEBUG"]:
        if not user_datastore.get_user('testuser@avrami.me'):
            user_datastore.create_user(email='testuser@avrami.me', password=hash_password('signmeup'))
            db.session.commit()


def require_auth_token(fn):
    def wrapper(*args, **kwargs):
        token = request.headers.get("authorization")
        if not token.startswith("Bearer "):
            raise Unauthorized("You must include an authorization token to continue")
        token = token[len("Bearer "):]
        user, payload = User.decode_auth_token(token)
        login_user(user)
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper
