from fastapi import APIRouter

# 创建路由器
product_router = APIRouter()

# 注册路由（接口）
@product_router.get("/search")
async def search():
    return {"search": "111"}

@product_router.get("/list")
async def list():
    return {"search": "222"}
