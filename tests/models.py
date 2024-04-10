import peewee
from db import db


class User(peewee.Model):
    name = peewee.CharField()

    class Meta:
        database = db


db.create_tables([User])
