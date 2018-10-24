import os

from peewee import Model, MySQLDatabase, SqliteDatabase, Database, Proxy, OperationalError

db: Proxy = Proxy()


class BaseModel(Model):
    class Meta:
        database: Database = db


def setup(app):
    """
    This function initializes the relevant database
    :param app: The flask app; we only need the config to determine our provider
    :return: None
    """
    global db
    database = None
    if app.config["PROVIDER"] == "DB_REMOTE":
        try:
            name = app.config["DB_NAME"]
            host = app.config["DB_HOST"]
            user = app.config["DB_USER"]
            password = app.config["DB_PWD"]
            database = MySQLDatabase(name, host=host, user=user, password=password)
            print("Using remote database")
        except OperationalError as ignored:
            # If we can't connect to the database fallback to a local database.
            app.config["PROVIDER"] = "DB_LOCAL"
            print("Connection to remote failed; Using fallback.")
    if app.config["PROVIDER"] == "DB_LOCAL":
        database = SqliteDatabase(os.path.join(os.path.dirname(__file__), "local.db"))
        print("Using Local Database")

    with database:
        print(database.get_tables())
    db.initialize(database)


def before_request():
    """
    Connect before a request.
    :return:
    """
    global db
    db.connect()


def after_request():
    """
    After the request close the connection
    :return:
    """
    global db
    if not db.is_closed():
        db.close()
