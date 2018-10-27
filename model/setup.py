from model.base import BaseModel, _database
from model.student import Student
from model.club import Club
from model.registration import Registration
from model.request import Request


def setup():
    BaseModel.setup()
    with _database:
        _database.create_tables([
            Student,
            Club,
            Registration,
            Request
        ])


if __name__ == "__main__":
    setup()
