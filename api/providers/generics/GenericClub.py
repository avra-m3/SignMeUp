from providers.generics.GenericRegistration import GenericRegistration


class GenericClub:
    """
    This object is an abstract class providing the methods and return types a club object should implement.
    """
    name: str

    def __init__(self, club_id):
        self.name = club_id
