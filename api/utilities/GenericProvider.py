import json


class GenericRegistration:
    """
    This abstract class implements methods required for a registration object
    """
    card_id: str  # The id of the card this registration is tied to or None if no id was found.
    club_id: str
    status: str  # 'complete', 'failed', 'queued', 'running', or 'created'
    message: str  # Explanatory string to accompany status.

    user_id: str  # None if processing in progress
    first_name: str  # ^^
    last_name: str  # ^^

    def __init__(self, club_id, card_id):
        """
        You should override this constructor to setup the object.
        :param card_id:
        """
        self.club_id = club_id
        self.card_id = card_id
        self.status = None
        self.message = None

        self.user_id = None
        self.first_name = None
        self.last_name = None
        pass

    def update(self):
        """
        updates this registration to match the current object
        :return:
        """
        raise NotImplementedError()

    @property
    def json(self):
        """
        This property converts the
        :return:
        """
        data = {
            "card_id": self.card_id,
            "status": self.status,
            "message": self.message,
            "results": None
        }

        if self.user_id is not None:
            data["results"] = {
                "user_id": self.user_id,
                "first_name": self.first_name,
                "last_name": self.last_name,
            }

        return data


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

    def get_registration(self, card_id) -> GenericRegistration:
        """
        Accepts a card id and returns the matching registration
        :param card_id: ..
        :return: A registration object if one is found
        :raises: NotFound error if no matching card is found.
        """
        raise NotImplementedError()


class GenericProvider:
    """
    This generic provider is an abstract class that provides methods for retrieving and storing data
    """

    def club(self, name) -> GenericClub:
        """
        This method when given a club name should return or create the matching club.
        :param name: The name/id assigned to the club
        :return: A Generic Club object
        """
        raise NotImplementedError()
