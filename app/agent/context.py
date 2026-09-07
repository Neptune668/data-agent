"""定义 langgraph 运行上下文（不可变依赖）。"""

from typing import TypedDict

from app.repositories.es.value_es_repository import ValueEsRepository
from app.repositories.mysql.dw_mysql_repository import DWMySQLRepository
from app.repositories.mysql.meta_mysql_repository import MetaMySQLRepository
from app.repositories.qdrant.column_qdrant_repository import ColumnQdrantRepository
from app.repositories.qdrant.metric_qdrant_repository import MetricQdrantRepository


class Context(TypedDict, total=False):
    """LangGraph 上下文：各节点共享的不可变依赖。"""
    dw_mysql_repo: DWMySQLRepository
    meta_mysql_repo: MetaMySQLRepository
    value_es_repo: ValueEsRepository
    column_qdrant_repo: ColumnQdrantRepository
    metric_qdrant_repo: MetricQdrantRepository
