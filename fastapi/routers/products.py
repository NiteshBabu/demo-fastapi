from fastapi import Body, APIRouter, status, Response, Query, Depends
from typing_extensions import Annotated
from models import Product, Category
import http

# using python's in-built http code as fastapi intellisense not working
HTTPStatus = http.HTTPStatus

router = APIRouter()


@router.get(
    "/products",
)
async def get_products():
    return [
        {
            "name": product.name,
            "price": product.price,
            "quantity": product.quantity,
            "category": Category.get(product.category).name,
        }
        for product in Product.select()
    ]


@router.get(
    "/product/{id}",
)
async def get_product_by_id(id: int, response: Response):
    product = Product.get_or_none(id)
    if not product:
        response.status_code = HTTPStatus.NOT_FOUND
        return {"error": "User not found"}
    return product


@router.post(
    "/product",
)
async def get_products(name: str, price: float, quantity: int):
    product = Product(name=name, price=price, quantity=quantity)
    product.save()
    return product


@router.patch("/product/{id}", status_code=HTTPStatus.OK)
async def update_product(
    id: int, name: str, price: float, quantity: int, category: str, response: Response
):
    product = Product.get_or_none(
        id,
    )
    if product:
        if name != None:
            product.name = name
        if price != None:
            product.price = price
        if quantity != None:
            product.quantity = quantity
        if Category.get_by_id(category):
            product.category = category
        product.save()
    if product:
        return product
    else:
        response.status_code = HTTPStatus.NOT_FOUND
        return {"error": "Product not found"}


@router.delete("/product/{id}", status_code=HTTPStatus.OK)
async def delete_product(id: int, response: Response):
    product = Product.delete_by_id(id)
    if product:
        return {"deleted": f"{product}"}
    else:
        response.status_code = HTTPStatus.NOT_FOUND
        return {"error": "Product not found"}
