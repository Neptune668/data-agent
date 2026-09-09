from contextlib import asynccontextmanager

import uvicorn

from pydantic import BaseModel
import anyio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from app.api.test.product_router import product_router
from app.api.test.order_router import order_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('服务启动时执行，做一次性的初始化工作')

    yield

    print('服务关闭前执行，做一次性的收尾工作')
app = FastAPI(lifespan=lifespan)


@app.get("/api/user/{cid}")
async def get_user(user_id: int):
    return {"user_id": user_id}


@app.post("/api/users/{cid}")
async def get_cid_wd(cid: str, wd: str):
    # 1.path参数
    # 2。query参数
    return {"cid": cid, "wd": wd}


class MyBody(BaseModel):
    name: str
    age: int
    sex: str


@app.post("/hello")
async def get_cid_wd(body: MyBody):
    # 1.path参数
    # 2。query参数
    return body


app.include_router(order_router, prefix="/api/order", tags=["订单管理"])
app.include_router(product_router, prefix="/product/order", tags=["产品管理"])


# 流式响应
async def fake_video_streamer():
    for i in range(10):
        yield 'data: {"name":"张三","age":23}\n\n'
        await anyio.sleep(1)


@app.get("/stream")
async def main():
    return StreamingResponse(fake_video_streamer(),media_type="text/event-stream")


if __name__ == '__main__':
    # 1.在终端进入当前目录执行 fastapi dev (自动刷新)

    # 2.使用uvicorn启动服务
    uvicorn.run(app, host='127.0.0.1', port=8001)

    # 3.执行命令
    # uvicorn main:app
