from providers.generics.GenericClub import GenericClub


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