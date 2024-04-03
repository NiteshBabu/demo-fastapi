from fastapi import Header, HTTPException
from typing_extensions import Annotated


async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "0000":
        raise HTTPException(status_code=400, detail="❌ No x-token header found ❌")
