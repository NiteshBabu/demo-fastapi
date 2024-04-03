from fastapi import Body, APIRouter, status, Response, Query, Depends
from typing_extensions import Annotated
from models import User, Security
import http

# using python's in-built http code as fastapi intellisense not working
HTTPStatus = http.HTTPStatus

router = APIRouter()


# @router.get("/items/")
# async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {"token": token}


@router.get("/")
async def root():
    return {"message": "Hello World 🔥"}


@router.get("/users")
async def get_users():

    return [
        {"name": f"{user.first_name} {user.last_name}", "email": user.email}
        for user in User.select()
    ]


@router.post(
    "/user",
)
async def create_user(
    first_name: str, last_name: str, email: str, birthday: str, password: str
):
    # print(type(datetime.datetime.strptime(birthday, "%d/%m/%y").date()))
    if User.filter(email=email):
        return {"error": "User already exists"}
    # if not datetime.datetime.strptime(birthday, "%d/%m/%y"):
    #     return {"error": "datetime not correct"}

    # user = User(name=user.name, birthday=time.strftime("%Y-%m-%d", time.localtime()))
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        birthday=birthday,
    )
    user.save()
    security = Security(user=user, password=password)
    security.save()
    return user
