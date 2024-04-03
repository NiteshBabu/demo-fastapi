from fastapi import Body, APIRouter, status, Response, Query, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from models import User, Security
from pydantic import BaseModel
import http
import datetime
import secrets

# using python's in-built http code as fastapi intellisense not working
HTTPStatus = http.HTTPStatus
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def fake_decode_token(token):
    return User(first_name=token + "fakedecoded", email="john@example.com")


async def get_current_user(response: Response, token: str = Depends(oauth2_scheme)):
    print(security)
    security = Security.get_or_none(token=token)
    # if not user:
    #     raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Unauthorized")

    # return user


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


class LoginCreds(BaseModel):
    email: str
    password: str


@router.post("/auth/token")
async def get_token(response: Response, login_creds: LoginCreds):
    user = User.get_or_none(email=login_creds.email)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User doesn't exist"
        )

    security = Security.get(user_id=user.id)

    if not security:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User doesn't exist"
        )

    if security.password == login_creds.password:
        if security.token and security.expire_time > datetime.datetime.now():
            return security.token

        security.token = secrets.token_hex(30)
        security.expire_time = datetime.datetime.now() + datetime.timedelta(seconds=10)
        security.save()
        return security.token

    raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Wrong Credentials")
