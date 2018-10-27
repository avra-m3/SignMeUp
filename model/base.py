import os
from datetime import datetime

import flask
from peewee import Proxy, Model, SqliteDatabase, DateTimeField, TimestampField, Database

database = _database = Proxy()


class BaseModel(Model):
    created_at = DateTimeField(default=datetime.now())
    modified_at = TimestampField()

    class Meta:
        database = _database

    @staticmethod
    def setup():
        db_path = os.path.join(os.path.dirname(__file__), "local.db")
        temp = SqliteDatabase(db_path)
        _database.initialize(temp)

