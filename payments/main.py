from fastapi import FastAPI, Request, HTTPException
from fastapi.background import BackgroundTasks
from models import Order 
import requests, time, json, http
from producer import publish_order


HTTPStatus = http.HTTPStatus

def format_order(order):
    return {
        "status": order.status,
		"order_date": str(order.order_date),
		"quantity": order.quantity,
		"products": order.products,
		"price": order.price,
		"fee": order.fee,
		"total": order.total,
		"id": order.id,
    }


app = FastAPI(
    title="Payments 💰",
    description="Payment Interface",
    # dependencies=[Depends(get_token_header)],
    version="0.1",
)


@app.get("/orders")
async def get():
    print(len(Order.select()))
    return [format_order(order) for order in  Order.select()]

@app.post("/orders")
async def create(request: Request, background_tasks : BackgroundTasks):
    body = await request.json()

    resp = requests.get(
        f"http://localhost:8000/product/{body["product_id"]}", headers={"x-token": "0000"}
    ).json()

    if resp["quantity"] >= body["quantity"]:
        order = Order(**body, 
                    products = body["product_id"],
                    price=resp['price'] * body["quantity"],
                    fee = .1 * resp["price"], 
                    total = resp['price'] * body["quantity"] + (0.1*resp["price"]))

        order.save()
        publish_order(format_order(order))
    # background_tasks.add_task(clear_order, order)
    # clear_order(order)
        return format_order(order)
    else:
        raise HTTPException(status_code=HTTPStatus.NOT_IMPLEMENTED, detail="Product in stock is less than ordered quantity")

def clear_order(order: Order):
    time.sleep(5)
    # order = Order.get(order)
    order.status = "CONFIRMED"
    order.save()
    print(order)


