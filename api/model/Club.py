from main import database as db


class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    registrations = db.relationship("Registration")