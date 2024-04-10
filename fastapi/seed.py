from fastapi.db.models import User, Product, Category
import faker
import random

fake = faker.Faker()


def seed_users():
    for user in User.select():
        User.delete_by_id(user)
    user = User(
        first_name="Nitesh",
        last_name="Babu",
        email="nitesh@gmail.com",
        birthday=fake.date_between(start_date="-18y", end_date="today"),
    )
    user.save()
    for _ in range(10):
        user = User(
            first_name=fake.unique.first_name(),
            last_name=fake.unique.last_name(),
            email=fake.unique.email(),
            birthday=fake.date_between(start_date="-18y", end_date="today"),
        )
        user.save()


def seed_category():
    for category in Category.select():
        Category.delete_by_id(category)
    for _ in range(10):
        category = Category(
            name=f"{fake.unique.state()}",
        )
        category.save()


def seed_products():
    for product in Product.select():
        Product.delete_by_id(product)

    categories = Category.select()
    for _ in range(10):
        product = Product(
            name=f"{fake.company()}",
            quantity=fake.random_int(min=1, max=10),
            price=fake.random_int(min=1, max=100),
            category=random.choice(categories),
        )
        product.save()


# seed_users()
# seed_category()
# seed_products()


user = User.select().first()
user.password = "NiteshBabu"
user.save()
