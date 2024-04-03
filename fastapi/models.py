from peewee import *
from db import db
import datetime


class User(Model):

    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    email = CharField(unique=True)
    birthday = DateField(null=True)

    class Meta:
        database = db


class Category(Model):
    name = CharField(max_length=50, unique=True)

    class Meta:
        database = db


class Product(Model):

    name = CharField(max_length=50)
    quantity = IntegerField(default=0)
    price = DecimalField(null=False)
    category = ForeignKeyField(Category, on_delete="cascade", null=True)

    class Meta:
        database = db


class Security(Model):
    user = ForeignKeyField(User, backref="security")
    token = CharField(max_length=255, null=True)
    password = CharField(max_length=255)
    expire_time = DateTimeField(
        default=datetime.datetime.now() + datetime.timedelta(seconds=60)
    )
    is_active = BooleanField(default=True)
    is_superuser = BooleanField(default=False)

    class Meta:
        database = db


db.create_tables([User, Product, Category, Security])
