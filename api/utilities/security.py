from flask_security import Security, SQLAlchemyUserDatastore

from model import Role
from model import User
from model.database import db


def setup(app):
    """
    Setup Flask Security
    :param app: The Flask Application Object
    :return: None
    """
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    Security(app, user_datastore)

    if app.config["DEBUG"]:
        if not user_datastore.get_user('testuser@avrami.me'):
            user_datastore.create_user(email='testuser@avrami.me', password='signmeup')
            db.session.commit()

