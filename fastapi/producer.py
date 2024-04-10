import pika, json

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# queue = channel.queue_declare("order_notify")
# queue_name = queue.method.queue


# channel.queue_bind(exchange="order", queue=queue_name, routing_key="order.notify")


def publish_order_status(order, status):
    channel.basic_publish(
        exchange="order",
        routing_key="order.status",
        body=json.dumps({"order": order, "status": status}),
    )
