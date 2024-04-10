from peewee import *
from db import db
from datetime import datetime

ORDER_STATUS = {"PENDING": "PENDING", "CONFIRMED": "CONFIRMED", "REFUNDED": "REFUNDED"}


class Order(Model):
    products = CharField()
    quantity = IntegerField()
    price = FloatField()
    fee = FloatField()
    total = FloatField()
    order_date = DateTimeField(default=datetime.now)
    status = CharField(default=ORDER_STATUS["PENDING"])

    class Meta:
        database = db


db.create_tables([Order])
