from flask_security import RoleMixin

from model import BaseModel
from model.database import db


class Role(BaseModel, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    _default_fields = ["id", "name", "description"]

