from providers.generics.GenericRegistration import GenericRegistration


class GenericClub:
    """
    This object is an abstract class providing the methods and return types a club object should implement.
    """
    name: str

    def __init__(self, club_id):
        self.name = club_id

    def register(self, card_id) -> GenericRegistration:
        """
        Accepts a card id and returns a GenericRegistration object with the given card id and the status created
        This method should also create any relevant information in the database.
        :param card_id: The card_id of the card being created.
        :return: The newly created registration
        :raises: Conflict if the registration already exists for this club.
        """
        raise NotImplementedError()

    def registration(self, card_id) -> GenericRegistration:
        """
        Accepts a card id and returns the matching registration if one exists. Will NOT create a missing registration.
        :param card_id: ..
        :return: A registration object if one is found
        :raises: NotFound error if no matching card is found.
        """
        raise NotImplementedError()
