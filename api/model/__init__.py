import json

from flask_sqlalchemy import SQLAlchemy

from model.Club import Club
from model.Registration import Registration
from model.Role import Role
from model.User import User

database = None


def setup(app):
    global database

    database = SQLAlchemy(app)
    database.create_all()
    creator_role = Role(name="creator", description="Able to create new enrolments into clubs")
    database.session.add(creator_role)
    database.session.commit()


__all__ = ["Role", "User", "Club", "BaseModel", "Registration", "setup", "database"]
