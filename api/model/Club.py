from model.database import db


class Club(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), unique=True)
    abbreviation = db.Column(db.String(255), unique=True)
    logo = db.Column(db.String(255))
    description = db.Column(db.String(255), default="")

    registrations = db.relationship("Registration")

    _default_fields = ["name", "id", "description", "logo", "abbreviation"]
