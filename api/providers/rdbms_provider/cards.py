import re

from peewee import CharField

from providers.rdbms_provider.Model import BaseModel


class Card(BaseModel):
    id: CharField(primary_key=True)
    first_name: CharField(default=None)
    last_name: CharField(default=None)

    @property
    def user_id(self):
        """ We can just derive the user_id from the card_id."""
        return re.match("21259(\d{7})\d{2}", self.id).groups()[0]
