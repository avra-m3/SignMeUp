from flask import app

from providers.rdbms_provider import base
from providers.rdbms_provider.card import Card
from providers.rdbms_provider.club import Club
from providers.rdbms_provider.registration import Registration


def setup(context):
    """
    Setup the database including migrations; creates etc.
    :param context: The context so we know which configuration to target
    :return: None
    """
    app.config = context
    base.setup(app)
    # Connect
    with base.db as database:
        database.create_tables([Card])
        database.create_tables([Club])
        database.create_tables([Registration])
        print(base.db.get_tables())


if __name__ == "__main__":
    setup({
        "PROVIDER": "DB_LOCAL",
        "DB_NAME": "signups",
        "DB_HOST": None,
        "DB_USER": None,
        "DB_PWD": None,
    })
