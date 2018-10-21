import os

import pymysql as pymysql
from werkzeug.contrib.cache import SimpleCache

from providers.rdbms_provider.club import Club
from utilities.GenericProvider import GenericProvider, GenericClub


class DBProvider(GenericProvider):
    def club(self, name) -> GenericClub:
        """
        :param name: The name of the club
        :return: A club implementing the Generic club interface
        """
        return Club.get_or_create(name=name)