from model.base import BaseModel, SQLITE
from model.student import Student
from model.club import Club
from model.registration import Registration


def setup():
    BaseModel.setup({
        "DATABASE": SQLITE
    })
    Student.create_table(True)
    Club.create_table(True)
    Registration.create_table(True)


if __name__ == "__main__":
    setup()
