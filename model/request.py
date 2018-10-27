import re

from peewee import CharField

from model.base import BaseModel


class Request(BaseModel):
    # These fields do not link to the models.
    card_number = CharField(14)
    club_name = CharField(64)

    workflow_state = CharField(8, default="created")
    errors = CharField(256, default=None, null=True)

    image_location = CharField(256)

    @property
    def user_id(self):
        return re.match("21259(\d{7})\d{2}", str(self.card_number)).groups()[0]
