from peewee import CharField, IntegrityError

from providers.rdbms_provider.Model import BaseModel
from providers.rdbms_provider.registration import Registration
from utilities.GenericProvider import GenericClub, GenericRegistration
from utilities.exception_router import Conflict


class Club(GenericClub, BaseModel):
    name: CharField(column_name="id", primary_key=True)
    username: CharField(default=None)
    password: CharField(default=None)

    def __init__(self, club_id):
        GenericClub.__init__(self, club_id=club_id)
        BaseModel.__init__(self, club_id=club_id)

    def register(self, card_id) -> GenericRegistration:
        result = Registration(club_id=self.name, card_id=card_id)
        try:
            result.save()
        except IntegrityError:
            raise Conflict

    def get_registration(self, card_id) -> GenericRegistration:
        return Registration.get(club_id=self.name, card_id=card_id)
