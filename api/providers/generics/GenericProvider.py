from providers.generics import GenericRegistration
from providers.generics.GenericClub import GenericClub


class GenericProvider:
    """
    This generic provider is an abstract class that provides methods for retrieving and storing data
    """

    def club(self, name: str) -> GenericClub:
        """
        This method when given a club name should return or create the matching club.
        :param name: The name/id assigned to the club
        :return: A Generic Club object
        """
        raise NotImplementedError()

    def register(self, club: GenericClub, card_id: str) -> GenericRegistration:
        """
        Accepts a card id and returns a GenericRegistration object with the given card id and the status created
        This method should also create any relevant information in the database.
        :param club: The club to attach this registration to.
        :param card_id: The card_id of the card being created.
        :return: The newly created registration
        :raises: Conflict if the registration already exists for this club.
        """
        raise NotImplementedError()

    def registration(self, club: GenericClub, card_id: str) -> GenericRegistration:
        """
        Accepts a card id and returns the matching registration if one exists. Will NOT create a missing registration.
        :param club: The club the registration is associated with
        :param card_id: ..
        :return: A registration object if one is found
        :raises: NotFound error if no matching card is found.
        """
        raise NotImplementedError()
