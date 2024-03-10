from fastapi import APIRouter, Request
from websockets import connect

router = APIRouter()


@router.get("/hello")
async def hello_world(request: Request):
    return "Hello World!"
