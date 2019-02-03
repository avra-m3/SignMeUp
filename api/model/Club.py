from model.database import db


class Club(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), unique=True)
    registrations = db.relationship("Registration")

    _default_fields = ["name"]
