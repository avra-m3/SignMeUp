from flask_login import UserMixin

from model import BaseModel
from model.database import db

# Define models
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class User(BaseModel, UserMixin):
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
