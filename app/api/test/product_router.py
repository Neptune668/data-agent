from fastapi import APIRouter

product_router = APIRouter()


@product_router.get("/search")
async def search():
    return {"search": "111"}


@product_router.get("/list")
async def list():
    return {"search": "222"}
