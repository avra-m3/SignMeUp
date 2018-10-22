import os

from providers.simple_provider.registration import FileRegistration
from modules.path_constants import PATHS
from providers.generics.GenericProvider import GenericProvider
from providers.generics.GenericClub import GenericClub
from providers.generics.GenericRegistration import GenericRegistration
from utilities.exception_router import NotFound, Conflict


class FileProvider(GenericProvider):
    def club(self, name) -> GenericClub:
        return ClubFaker(name)


class ClubFaker(GenericClub):
    """
    This provider doesn't allow for club-based registration.
    """

    def registration(self, card_id) -> GenericRegistration:
        fpath = os.path.join(PATHS.OUTPUT, "{}_{}".format(self.name, card_id))
        if os.path.isfile(fpath):
            return FileRegistration(self.name, card_id)
        raise NotFound("The resource was not found.")

    def register(self, card_id) -> GenericRegistration:
        fpath = os.path.join(PATHS.OUTPUT, "{}_{}".format(self.name, card_id))
        if os.path.exists(fpath):
            raise Conflict("The resource already exists.")
        return FileRegistration(self.name, card_id)
