import datetime


def attempt_recognition(provider, path: str):
    result = provider(path)
    from modules.ocr.process import get_card_data
    data = get_card_data(result)

    return User(data["user"]), Card(data["card"])


class User:
    student_id: str
    first_name: str
    last_name: str
    email: str
    source: dict

    def __init__(self, data):
        self.student_id = data["student_id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.source = data


class Card:
    expiry: datetime.datetime

    def __init__(self, data):
        self.expiry = data["expiry"]
