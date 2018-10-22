import pymysql
from peewee import ForeignKeyField, CharField, CompositeKey

from providers.rdbms_provider.Model import BaseModel
from providers.rdbms_provider.cards import Card
from providers.rdbms_provider.club import Club
from providers.generics.GenericRegistration import GenericRegistration


class Registration(GenericRegistration, BaseModel):
    card_id = ForeignKeyField(Card, backref='card_id')
    club_id = ForeignKeyField(Club, backref='club_id')
    status = CharField(default="created")
    message = CharField(default="The resource was successfully created")

    class Meta:
        primary_key = CompositeKey('card_id', 'club_id')

    def __init__(self, club_id, card_id):
        BaseModel.__init__(self, card_id=card_id, club_id=club_id)

    def update(self):
        self.save()

    @property
    def user_id(self):
        return self.card_id.user_id

    @property
    def first_name(self):
        return self.card_id.first_name

    @property
    def last_name(self):
        return self.card_id.last_name
