from typing import TypedDict

from langchain_huggingface import HuggingFaceEndpointEmbeddings

from app.repositories.es.value_es_repository import ValueEsRepository
from app.repositories.mysql.dw_mysql_repository import DWMySQLRepository
from app.repositories.mysql.meta_mysql_repository import MetaMySQLRepository
from app.repositories.qdrant.column_qdrant_repository import ColumnQdrantRepository
from app.repositories.qdrant.metric_qdrant_repository import MetricQdrantRepository


# 定义上下文依赖数据模型（类型）
class DataAgentContext(TypedDict):
    # agent的上下文依赖数据
    value_es_repo: ValueEsRepository
    dw_mysql_repo: DWMySQLRepository
    meta_mysql_repo: MetaMySQLRepository
    column_qdrant_repo: ColumnQdrantRepository
    metric_qdrant_repo: MetricQdrantRepository
    embedding_client: HuggingFaceEndpointEmbeddings
