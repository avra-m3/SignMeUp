from peewee import Model, MySQLDatabase, SqliteDatabase, Database


class BaseModel(Model):
    class Meta:
        database: Database = None


def setup(app):
    if app.config["PROVIDER"] == "DB_REMOTE":
        name = app.config["DB_NAME"]
        host = app.config["DB_HOST"]
        user = app.config["DB_USER"]
        password = app.config["DB_PWD"]
        BaseModel.Meta.database = MySQLDatabase(name, host=host, user=user, password=password)
    elif app.config["PROVIDER"] == "DB_LOCAL":
        BaseModel.Meta.database = SqliteDatabase("")


def before_request():
    BaseModel.Meta.database.connect()


def after_request():
    if not BaseModel.Meta.database.is_closed():
        BaseModel.Meta.database.close()
