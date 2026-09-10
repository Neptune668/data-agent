import uuid

import uvicorn
from fastapi import FastAPI, Request

from app.api.routers.query_router import query_router
from app.core.context import set_req_id
from app.core.lifespan import lifespan

# 创建FastAPI应用
app = FastAPI(lifespan=lifespan)

# 注册路由器
app.include_router(query_router)

# 中间件
# 针对 每次http请求
@app.middleware("http")
async def middle_ware(request: Request, call_next):
    # print('每次处理请求前执行。。。。。。')

    # 给每个请求添加一个唯一的请求id
    set_req_id(uuid.uuid4())

    response = await call_next(request) # 调用下一个中间件或目标路由函数

    # print('。。。。。。每次处理请求后执行')

    return response
# /* select#1 */ select `dw`.`d`.`province` AS `province`,sum(`dw`.`f`.`order_amount`) AS `sales_amount`
# from `dw`.`fact_order` `f` join `dw`.`dim_region` `d`
# where ((`dw`.`d`.`region_id` = `dw`.`f`.`region_id`) and (`dw`.`d`.`region_name` = '华北')) group by `dw`.`d`.`province` order by `sales_amount` desc limit 3

if __name__ == '__main__':
    uvicorn.run(app,host='127.0.0.1',port=8008)
