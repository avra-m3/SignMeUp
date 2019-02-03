from model import BaseModel
from model import database as db


class Registration(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    club = db.Column(db.Integer, db.ForeignKey('club.id'))
    evidence = db.Column(db.String)
    expiry = db.Column(db.DateTime)
