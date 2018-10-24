from peewee import CharField

from providers.generics.GenericClub import GenericClub
from providers.rdbms_provider.base import BaseModel


class Club(GenericClub, BaseModel):
    name = CharField(primary_key=True)
    username = CharField(default="")
    password = CharField(default="")

    def __init__(self, name):
        BaseModel.__init__(self, name=name)

    class Meta:
        pass
