from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import routers.users as users
from routers import login, products
from dependencies import get_token_header

app = FastAPI(
    title="Demo By Nick 🔥",
    description="This is a simple CRUD application",
    dependencies=[Depends(get_token_header)],
    version="0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(users.router)
app.include_router(login.router)
app.include_router(products.router)
