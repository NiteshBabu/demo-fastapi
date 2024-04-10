from models import Order
import faker
from datetime import datetime

fake = faker.Faker()


def seed_orders():
    for order in Order.select():
        Order.delete_by_id(order)

    # for _ in range(10):
    #     order = Order(
    #         products=5,
    #         quantity=fake.random_int(min=1, max=5),
    #         price=100,
    #         fee=10,
    #         total=110,
    #         order_date=datetime.now(),
    #         status="pending",
    #     )

    #     order.save()


seed_orders()
