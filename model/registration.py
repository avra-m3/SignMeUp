from datetime import datetime

from peewee import ForeignKeyField, CharField, CompositeKey

from model.base import BaseModel
from model.student import Student
from model.club import Club


class Registration(BaseModel):
    user_id = ForeignKeyField(Student, backref="id")
    club_id = ForeignKeyField(Club, backref="id")
    year = CharField(4, default=datetime.now().year)
    proof = CharField(256, null=False)

    class Meta:
        primary_key = CompositeKey('user_id', 'club_id', 'year')
