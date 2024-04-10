from db.models import Product, Category
import pika, json, time
from producer import publish_order_status

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

queue = channel.queue_declare("order_notify")
queue_name = queue.method.queue


channel.queue_bind(exchange="order", queue=queue_name, routing_key="order.notify")


def callback(ch, method, properties, body):

    print("[X] Product Order Hit")
    time.sleep(4)
    payload = json.loads(body)
    product = Product.get_or_none(payload["products"])
    if product:
        if product.quantity >= payload["quantity"]:
            product.quantity -= payload["quantity"]
            product.save()
            publish_order_status(payload, "CONFIRMED")
            print("Product Updated")
        else:
            publish_order_status(payload, "REFUNDED")
            print("Out of Stock")

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(on_message_callback=callback, queue=queue_name)

print("[X] Waiting for Messages -->")
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

# header, method, body = channel.basic_get("order_notify")
# def on_message(channel, method_frame, header_frame, body):
#     print(method_frame.delivery_tag)
#     print(body)
#     print()
#     channel.basic_ack(delivery_tag=method_frame.delivery_tag)
