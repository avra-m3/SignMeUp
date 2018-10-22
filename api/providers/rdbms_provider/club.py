from peewee import CharField, IntegrityError, DoesNotExist

from providers.generics.GenericClub import GenericClub
from providers.generics.GenericRegistration import GenericRegistration
from providers.rdbms_provider.Model import BaseModel
from providers.rdbms_provider.registration import Registration
from utilities.exception_router import Conflict, NotFound


class Club(GenericClub, BaseModel):
    name: CharField(column_name="id", primary_key=True)
    username: CharField(default=None)
    password: CharField(default=None)

    def __init__(self, club_id):
        BaseModel.__init__(self, club_id=club_id)

    def register(self, card_id) -> GenericRegistration:
        """
        Attempt to create the registration, if the database rejects with an Integrity Error throw a Conflict.
        :param card_id: The id of the card being created
        :return: The result
        :raises: Conflict if a record exists for the same card in the same club.
        """
        result = Registration(club_id=self.name, card_id=card_id)
        try:
            result.save()
            return result
        except IntegrityError:
            raise Conflict("Attempted to register a registration that already exists.")

    def registration(self, card_id) -> GenericRegistration:
        """
        Attempt to retrieve a registration, if it does not exist throw a Not Found error.
        :param card_id: The barcode of the card to retrieve.
        :return:
        """
        try:
            return Registration.get(club_id=self.name, card_id=card_id)
        except DoesNotExist:
            # As per Generic API raise this exception although something is seriously fucked if it does.
            raise NotFound()
