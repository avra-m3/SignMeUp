import re

from peewee import CharField, DateField

from model.base import BaseModel


class Student(BaseModel):
    id = CharField(8, primary_key=True)
    first_name = CharField(128, null=False)
    last_name = CharField(128, null=False)
    expiry = DateField()