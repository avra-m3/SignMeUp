import os

from modules.path_constants import PATHS
from providers.generics.GenericClub import GenericClub
from providers.generics.GenericProvider import GenericProvider
from providers.generics.GenericRegistration import GenericRegistration
from providers.simple_provider.registration import FileRegistration
from utilities.exception_router import NotFound, Conflict


class FileProvider(GenericProvider):
    def registration(self, club: GenericClub, card_id: str) -> GenericRegistration:
        fpath = os.path.join(PATHS.OUTPUT, "{}_{}".format(club.name, card_id))
        if os.path.isfile(fpath):
            return FileRegistration(club.name, card_id)
        raise NotFound("The resource was not found.")

    def register(self, club: GenericClub, card_id: str) -> GenericRegistration:
        fpath = os.path.join(PATHS.OUTPUT, "{}_{}".format(club.name, card_id))
        if os.path.exists(fpath):
            raise Conflict("The resource already exists.")
        return FileRegistration(club.name, card_id)

    def club(self, name) -> GenericClub:
        return GenericClub(name)
