"""
FastAPI 生命周期事件

职责：
1. 定义服务启动时的一次性初始化工作
2. 定义服务关闭前的一次性收尾工作
3. 以 asynccontextmanager 形式提供给 FastAPI 的 lifespan 参数
"""
