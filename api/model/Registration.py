from model.base import BaseModel
from model.database import db


class Registration(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    club_id = db.Column(db.Integer(), db.ForeignKey('club.id'))

    evidence = db.Column(db.String(255))
    expiry = db.Column(db.DateTime)

    _default_fields = ["id", "expiry"]

    user = db.relationship("User")
    club = db.relationship("Club")

    def to_dict(self):
        response = BaseModel.to_dict(self)
        response["user"] = BaseModel.to_dict(self.user)
        response["club"] = BaseModel.to_dict(self.club)

        return response
