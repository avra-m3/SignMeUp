from peewee import CharField

from model.base import BaseModel


class Club(BaseModel):
    club_id = CharField(64, primary_key=True)
