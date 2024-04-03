from fastapi import FastAPI, Depends
import routers.users as users
from routers import login
from dependencies import get_token_header

app = FastAPI(
    title="Demo By Nick 🔥",
    description="This is a simple CRUD application",
    dependencies=[Depends(get_token_header)],
    version="0.1",
)

app.include_router(users.router)
app.include_router(login.router)
