from sqlite3 import connect
from peewee import SqliteDatabase


db = SqliteDatabase("db.sqlite")


db.connect()
