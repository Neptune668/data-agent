from fastapi import APIRouter

# 路由器
order_router = APIRouter()

# 注册路由（接口）
@order_router.get('/search')
async def search():
    return {"search": "111"}

@order_router.get('/list')
async def list():
    return {"search": "222"}

@order_router.get('/date')
async def date():
    return {"search": "333"}
