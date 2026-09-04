import asyncio
from contextvars import ContextVar

# 创建上下文变量
# 参数1：上下文变量名称
# 参数2：默认值，未设置值时返回'None'
_req_id_context_var = ContextVar('request_id', default='None')

# 设置请求id
def set_req_id(rid: str):
    _req_id_context_var.set(rid)

# 获取请求id
def get_req_id()->str:
    return _req_id_context_var.get()

# 测试
if __name__ == "__main__":

    # 测试同一个请求中操作
    async def test1():
        print("====在同一个请求中（也就是同一个循环任务中操作）===）")
        print(f"获取request_id={get_req_id()}")
        set_req_id(3)
        print(f"设置为3后获取reqeust_id={get_req_id()}")
        set_req_id(4)
        print(f"设置为4后获取reqeust_id={get_req_id()}")

    asyncio.run(test1())

    # 模拟请求1操作
    async def req1():
        print("执行请求1..。")
        print(f"获取request_id={get_req_id()}")
        set_req_id(5)
        print(f"设置为5后获取reqeust_id={get_req_id()}")

    # 模拟请求2操作
    async def req2():
        print("执行请求2..。")
        print(f"获取request_id={get_req_id()}")
        set_req_id(6)
        print(f"设置为6后获取reqeust_id={get_req_id()}")

    # 测试不同请求中操作
    async def test2():
        print("====在多个请求中（也就是多个循环任务中操作===")
        cor1 = req1()
        cor2 = req2()
        await asyncio.gather(cor1, cor2)

    asyncio.run(test2())