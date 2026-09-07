from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState, TableInfoState, MetricInfoState
from app.core.log import logger
from app.models.mysql.column_info_mysql import ColumnInfoMySQL
from app.models.qdrant.column_info_qdrant import ColumnInfoQdrant



def _convert_column_info_mysql_to_qdrant(column_info: ColumnInfoMySQL)->ColumnInfoQdrant:
    return ColumnInfoQdrant(
        id=column_info.id,
        name=column_info.name,
        type=column_info.type,
        description=column_info.description,
        role=column_info.role,
        table_id=column_info.table_id,
        alias=column_info.alias,
        examples=column_info.examples
    )

# 节点：合并召回信息
async def merge_recall(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    # 输出给前端的数据（前后端约定好的格式）
    runtime.stream_writer({"stage": "合并召回信息"})

    # recall_columns: list[ColumnInfoQdrant]  # 召回的字段信息列表
    # recall_metrics: list[MetricInfoQdrant]  # 召回的指标信息列表
    # recall_values: list[ValueInfoEs]  # 召回的字段取值列表

    recall_columns = state["recall_columns"]
    recall_metrics = state["recall_metrics"]
    recall_values = state["recall_values"]
    meta_mysql_repo = runtime.context["meta_mysql_repo"]

    # 合并后的数据
    table_infos: list[TableInfoState] = []
    metric_infos: list[MetricInfoState] = []

    # 收集完整的字段信息列表
    # 以recall_columns为主
    # 转成字典 {column_id: ColumnInfoQdrant} 去重
    column_infos_dict: dict[str,ColumnInfoQdrant] = {column['id']:column for column in recall_columns}

    # 补充：召回指标关联的字段
    for metric in recall_metrics:
        for column_id in metric["relevant_columns"]:
            if column_id not in column_infos_dict:
                # 如果当前字段不在召回字段信息列表中，去meta库查询该字段的信息
                column_info: ColumnInfoMySQL = await meta_mysql_repo.get_column_info_by_id(column_id)
                column_infos_dict[column_id] = _convert_column_info_mysql_to_qdrant(column_info)


    # 补充：召回字段取值对应的字段
    for value_info in recall_values:
        column_id = value_info["column_id"]
        if column_id not in column_infos_dict:
            # 如果当前字段不在召回字段信息列表中，去meta库查询该字段的信息
            column_info: ColumnInfoMySQL = await meta_mysql_repo.get_column_info_by_id(column_id)
            column_infos_dict[column_id] = _convert_column_info_mysql_to_qdrant(column_info)

        # 如果当前字段的值不在示例中，添加到示例中
        if value_info["value"] not in column_infos_dict[column_id]["examples"]:
            column_infos_dict[column_id]["examples"].append(value_info["value"])

    # 将字段信息列表按表分组
    # {table_id: list[ColumnInfoQdrant]}
    table_column_dict: dict[str,list[ColumnInfoQdrant]] = {}
    # column_infos_dict.values() -> list[ColumnInfoQdrant]
    for column in column_infos_dict.values():
        table_id = column["table_id"]
        if table_id not in table_column_dict:
            table_column_dict[table_id] = []
        table_column_dict[table_id].append(column)

    logger.info(f'table_column_dict：{table_column_dict}')



    # 补充：相关表的主外键字段

    # 更新状态数据
    return {"table_infos": '', "metric_infos": ''}
