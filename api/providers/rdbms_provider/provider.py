from providers.rdbms_provider.club import Club
from providers.generics.GenericProvider import GenericProvider
from providers.generics.GenericClub import GenericClub


class DBProvider(GenericProvider):
    def club(self, name) -> GenericClub:
        """
        :param name: The name of the club
        :return: A club implementing the Generic club interface
        """
        return Club.get_or_create(name=name)