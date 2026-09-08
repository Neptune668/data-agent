import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse

from app.api.order_router import order_router
from app.api.product_router import product_router

# 生命周期事件：
# 针对整个应用服务
@asynccontextmanager
async def lifespan(app: FastAPI):
    print('服务启动时执行，做一次性的初始化工作')

    yield

    print('服务关闭前执行，做一次性的收尾工作')


# 创建FastAPI的实例对象（app应用）
app = FastAPI(lifespan=lifespan)

# 注册路由（接口）
@app.get("/hello")
async def hello1():
    print('处理 /hello 的get请求')

    # 给前端响应内容
    return {"message": "hello world 11"}


@app.post("/hello")
async def hello2():
    print('处理 /hello 的post请求')

    # 给前端响应内容
    return {"message": "hello world 22"}


# 获取不同类型的参数：
# 1.path参数 （/hello/123）
# 2。query参数 （/hello?wd=456）
# 3。body参数（JSON格式）

@app.get("/api/users/{cid}")
async def get_user(cid: str):
    # 1.path参数
    return {'cid': cid}

@app.post("/api/users/{cid}")
async def get_cid_wd(cid: str, wd: str):
    # 1.path参数
    # 2。query参数
    return {"cid": cid, "wd": wd}

# 定义body参数的数据结构
class MyBody(BaseModel):
    name: str
    age: int
    gender: str

@app.post('/api/users')
async def post_user(body: MyBody):
    # 3。body参数（JSON格式）
    return body


# 使用路由器：
# 通常按业务分为不同的模块
# 注册路由器
app.include_router(order_router, prefix='/order')
app.include_router(product_router, prefix='/product')


# 流式响应
async def fake_video_streamer():
    for i in range(10):
        # 流式响应的数据格式：'data: 数据\n\n'
        yield 'data: {"name":"张三","age":23}\n\n'
        await asyncio.sleep(1)

@app.get("/stream")
async def main():
    return StreamingResponse(
        fake_video_streamer(),
        media_type="text/event-stream"
    )



if __name__ == '__main__':
    # 1.在终端进入当前目录执行 fastapi dev (自动刷新)

    # 2.使用uvicorn启动服务
    uvicorn.run(app, host='127.0.0.1', port=8001)

    # 3.执行命令
    # uvicorn main:app