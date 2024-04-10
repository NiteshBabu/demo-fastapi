# from peewee import SqliteDatabase
from db.models import db, User, Product, Category, Security


# db = SqliteDatabase("db.sqlite")
# db.connect()


def init():
    db.init("db.sqlite")
    db.create_tables([User, Product, Category, Security])
