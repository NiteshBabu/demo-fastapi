import pika, uuid, json, time

# credentials = pika.PlainCredentials("guest", "guest")
# params = pika.ConnectionParameters("127.0.0.1", "5672", "/", credentials)

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.exchange_declare(exchange="order", exchange_type="direct")

order = {"id": str(uuid.uuid4()), "name": "Nerf Gun", "quantity": 100}

# channel.basic_publish("exchange", "routing_key", "body")


def publish_order(order):
    channel.basic_publish(
        exchange="order", routing_key="order.notify", body=json.dumps(order)
    )
