from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.clients.embedding_client_manager import embedding_client_manager
from app.clients.es_client_manager import es_client_manager
from app.clients.mysql_client_manager import dw_mysql_client_manager, meta_mysql_client_manager
from app.clients.qdrant_client_manager import qdrant_client_manager


# 生命周期事件
# 针对 整个应用服务
@asynccontextmanager
async def lifespan(app: FastAPI):
    # print('服务启动时执行，做一次性的初始化工作')

    # 初始化客户端
    es_client_manager.init()
    qdrant_client_manager.init()
    dw_mysql_client_manager.init()
    meta_mysql_client_manager.init()
    embedding_client_manager.init()

    yield

    # print('服务关闭前执行，做一次性的收尾工作')

    # 关闭客户端
    await es_client_manager.close()
    await qdrant_client_manager.close()
    await dw_mysql_client_manager.close()
    await meta_mysql_client_manager.close()
