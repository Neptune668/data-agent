from typing import TypedDict

from app.models.es.value_info_es import ValueInfoEs
from app.models.qdrant.column_info_qdrant import ColumnInfoQdrant
from app.models.qdrant.metric_info_qdrant import MetricInfoQdrant


class ColumnInfoState(TypedDict):
    name: str
    type: str
    role: str
    examples: list
    description: str
    alias: list

class TableInfoState(TypedDict):
    name: str
    role: str
    description: str
    columns: list[ColumnInfoState]

class MetricInfoState(TypedDict):
    name: str
    description: str
    relevant_columns: list
    alias: list

# 定义state数据模型（类型）
class DataAgentState(TypedDict):
    # agent的状态数据
    query: str # 用户的提问
    sql: str # 生成的SQL
    error: str # 校验SQL的错误信息
    keywords: list[str] # 关键词
    recall_columns: list[ColumnInfoQdrant] # 召回的字段信息列表
    recall_metrics: list[MetricInfoQdrant] # 召回的指标信息列表
    recall_values: list[ValueInfoEs] # 召回的字段取值列表
    table_infos: list[TableInfoState] # 合并后的表信息列表
    metric_infos: list[MetricInfoState] # 合并后的指标信息列表