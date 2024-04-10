from models import Order
import pika, json, time

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

queue = channel.queue_declare("order_status")
queue_name = queue.method.queue


channel.queue_bind(exchange="order", queue=queue_name, routing_key="order.status")


def callback(ch, method, properties, body):
    print("[X] Order Status Hit")
    time.sleep(5)
    payload = json.loads(body)
    order = Order.get_or_none(payload["order"]["id"])
    if order:
        order.status = payload["status"]
        order.save()
        print(f"[{order.id}] Order Updated ", end="->")

    ch.basic_ack(delivery_tag=method.delivery_tag)
    if payload["status"] == "CONFIRMED":
        print("Confirmed")
    if payload["status"] == "REFUNDED":
        print("Refunded")


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
