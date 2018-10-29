import os
from abc import ABC
from datetime import datetime

from peewee import Model, SqliteDatabase, MySQLDatabase, DateTimeField, TimestampField, Database

SQLITE = "sqlite"
MYSQL = "mysql"
POSTGRE = "postgre"


class DynDatabase(Database, ABC):
    """
    This entire class is a giant hack to get around the retarded way peewee handles database creation/destruction.
    I Would not recommend attempting to modify this.
    """
    # The underlying private STATIC database, may be None do not call.
    _database: Database = None

    def __getattr__(self, item):
        """
        If for some reason someone (Cough peewee) attempts to access this class
        as a database. Then proxy the call to  _database
        :param item: The item to lookup
        :return: ?
        """
        return self.database.__getattribute__(item)

    # Private configuration (Private to avoid peeweee conflicts)
    type = SQLITE
    config = {}

    keep_alive = True

    def __init__(self):
        """
        Because we've inherited from Database we need to override the
        constructor as we aren't actually a database instance, we just
        quack like one :)
        """
        pass

    @staticmethod
    def _create(cls) -> Database:
        """
        Create a database based on the type/config
        :param cls: An instance of DynDatabase
        :return: An actual database
        """
        if cls.type == SQLITE:
            db_path = os.path.join(os.path.dirname(__file__), "local.db")
            return SqliteDatabase(db_path)
        elif cls.type == MYSQL:
            db = cls.config["name"]
            host = cls.config["host"]
            user = cls.config["username"]
            pwd = cls.config["password"]
            return MySQLDatabase(db, host=host, username=user, password=pwd)
        elif cls.type == POSTGRE:
            raise NotImplementedError("This implementation is left as an exercise to the reader.")
        raise RuntimeError("Invalid Database Requested.")

    @property
    def database(self):
        """
        Get/Create/Connect the current database.
        :return:
        """
        cls = DynDatabase
        if cls._database is None:
            cls._database = self._create(cls)
        if cls._database.is_closed():
            cls._database.connect()
        return cls._database

    def __get__(self, instance, owner) -> Database:
        return self.database

    @staticmethod
    def disconnect():
        """
        Disconnect the database (This may delete depending on implementation)
        :return:
        """
        cls = DynDatabase
        if cls._database is not None:
            cls._database.close()
            if not cls.keep_alive:
                cls._database = None


class BaseMeta:
    database = DynDatabase()


class BaseModel(Model):
    created_at = DateTimeField(default=datetime.now())
    modified_at = TimestampField()

    Meta = BaseMeta

    @staticmethod
    def setup(cfg: dict):
        database = DynDatabase()
        # Set the database type.
        database.type = cfg["DATABASE"] or SQLITE
        database.config = cfg["DATABASE_CONFIG"]

        def disconnect(r):
            database.disconnect()
            return r

        if "FLASK_APP" in cfg:
            cfg["FLASK_APP"].after_request(disconnect)
