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

    def update(self) -> None:
        """
        updates this registration to match the current object
        :return: None
        :raises: NotFound if the object does not exist.
        """
        raise NotImplementedError()

    @property
    def json(self) -> dict:
        """
        This property provides the registration as a dict object
        :return: self as a dictionary
        """
        data = {
            "card_id": self.card_id,
            "status": self.status,
            "message": self.message,
            "results": None
        }

        if self.first_name is not None and self.last_name is not None:
            data["results"] = {
                "user_id": self.user_id,
                "first_name": self.first_name,
                "last_name": self.last_name,
            }

        return data
