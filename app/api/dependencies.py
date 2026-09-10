from fastapi import Depends
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.embedding_client_manager import embedding_client_manager
from app.clients.es_client_manager import es_client_manager
from app.clients.mysql_client_manager import dw_mysql_client_manager, meta_mysql_client_manager
from app.clients.qdrant_client_manager import qdrant_client_manager
from app.repositories.es.value_es_repository import ValueEsRepository
from app.repositories.mysql.dw_mysql_repository import DWMySQLRepository
from app.repositories.mysql.meta_mysql_repository import MetaMySQLRepository
from app.repositories.qdrant.column_qdrant_repository import ColumnQdrantRepository
from app.repositories.qdrant.metric_qdrant_repository import MetricQdrantRepository
from app.services.query_service import QueryService


async def get_dw_session():
    async with dw_mysql_client_manager.session_factory() as session:
        # return session 返回session后，立即退出async with语句，自动关闭session
        yield session # yield session后，暂停执行当前程序，切换执行其他程序，当前数据库操作完成后，回到当前暂停的位置，继续往下执行，然后结束async with语句，自动关闭session

def get_dw_mysql_repo(session: AsyncSession = Depends(get_dw_session)):
    return DWMySQLRepository(session)



async def get_meta_session():
    async with meta_mysql_client_manager.session_factory() as session:
        # return session 返回session后，立即退出async with语句，自动关闭session
        yield session # yield session后，暂停执行当前程序，切换执行其他程序，当前数据库操作完成后，回到当前暂停的位置，继续往下执行，然后结束async with语句，自动关闭session

def get_meta_mysql_repo(session: AsyncSession = Depends(get_meta_session)):
    return MetaMySQLRepository(session)


def get_value_es_repo():
    return ValueEsRepository(es_client_manager.client)


def get_column_qdrant_repo():
    return ColumnQdrantRepository(qdrant_client_manager.client)


def get_metric_qdrant_repo():
    return MetricQdrantRepository(qdrant_client_manager.client)


def get_embedding_client():
    return embedding_client_manager.client

async def get_query_service(
    dw_mysql_repo: DWMySQLRepository = Depends(get_dw_mysql_repo),
    meta_mysql_repo: MetaMySQLRepository = Depends(get_meta_mysql_repo),
    value_es_repo: ValueEsRepository = Depends(get_value_es_repo),
    column_qdrant_repo: ColumnQdrantRepository = Depends(get_column_qdrant_repo),
    metric_qdrant_repo: MetricQdrantRepository = Depends(get_metric_qdrant_repo),
    embedding_client: HuggingFaceEndpointEmbeddings = Depends(get_embedding_client),
):
    return QueryService(
        dw_mysql_repo=dw_mysql_repo,
        meta_mysql_repo=meta_mysql_repo,
        value_es_repo=value_es_repo,
        column_qdrant_repo=column_qdrant_repo,
        metric_qdrant_repo=metric_qdrant_repo,
        embedding_client=embedding_client
    )
