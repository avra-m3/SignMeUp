import json
import os

from modules.path_constants import PATHS
from utilities.GenericProvider import GenericRegistration


class FileRegistration(GenericRegistration):

    def __init__(self, club_id, card_id):
        super().__init__(club_id, card_id)
        if os.path.exists(self.path):
            with open(self.path, "r") as fin:
                data = json.loads(fin.read())
                self.status = data["status"]
                self.message = data["message"]
                results = data["results"] or []
                if "user_id" in results:
                    self.user_id = results["user_id"]
                if "first_name" in results:
                    self.first_name = results["first_name"]
                if "last_name" in results:
                    self.last_name = results["last_name"]
        else:
            self.status = self.message = self.user_id = self.first_name = self.last_name = None
            self.update()

    def update(self):
        """
        Update an output file for a given id
        :return: None
        """
        with open(self.path, "w") as output:
            output.write(json.dumps(self.json))

    @property
    def path(self):
        return os.path.join(PATHS.OUTPUT, "{}_{}".format(self.club_id, self.card_id))