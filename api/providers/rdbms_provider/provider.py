from peewee import DoesNotExist
from peewee import IntegrityError

from providers.generics import GenericRegistration
from providers.generics.GenericClub import GenericClub
from providers.generics.GenericProvider import GenericProvider
from providers.rdbms_provider.card import Card
from providers.rdbms_provider.club import Club
from providers.rdbms_provider.registration import Registration
from utilities.exception_router import Conflict, NotFound


class DBProvider(GenericProvider):
    def club(self, name) -> GenericClub:
        """
        :param name: The name of the club
        :return: A club implementing the Generic club interface
        """
        try:
            club = Club.get(Club.name == name)
        except Club.DoesNotExist:
            club = Club.create(name=name)
        return club

    def register(self, club: GenericClub, card_id) -> GenericRegistration:
        """
        Attempt to create the registration, if the database rejects with an Integrity Error throw a Conflict.
        :param club: The club to attach the registration to
        :param card_id: The id of the card being created
        :return: The result
        :raises: Conflict if a record exists for the same card in the same club.
        """
        try:
            Card.create(id=card_id)
        except IntegrityError:
            pass
        try:
            result = Registration(club_id=club.name, card_id=card_id)
            result.save()
            return result
        except IntegrityError as ex:
            print(ex)
            raise Conflict("Attempted to register a registration that already exists.")

    def registration(self, club: GenericClub, card_id) -> GenericRegistration:
        """
        Attempt to retrieve a registration, if it does not exist throw a Not Found error.
        :param club: The club to retrieve this registration for.
        :param card_id: The barcode of the card to retrieve.
        :return:
        """
        try:
            return Registration.get(club_id=club.name, card_id=card_id)
        except DoesNotExist:
            # As per Generic API raise this exception although something is seriously fucked if it does.
            raise NotFound()
