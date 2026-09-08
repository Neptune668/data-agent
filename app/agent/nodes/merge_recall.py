from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState, TableInfoState, MetricInfoState, ColumnInfoState
from app.core.log import logger
from app.models.mysql.column_info_mysql import ColumnInfoMySQL
from app.models.mysql.table_info_mysql import TableInfoMySQL
from app.models.qdrant.column_info_qdrant import ColumnInfoQdrant
from app.models.qdrant.metric_info_qdrant import MetricInfoQdrant


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
def _convert_column_info_qdrant_to_state(column: ColumnInfoQdrant)->ColumnInfoState:
    return ColumnInfoState(
        name=column["name"],
        type=column["type"],
        role=column["role"],
        examples=column["examples"],
        description=column["description"],
        alias=column["alias"]
    )


def _convert_metric_info_qdrant_to_state(metric: MetricInfoQdrant)->MetricInfoState:
    return MetricInfoState(
        name=metric["name"],
        description=metric["description"],
        relevant_columns=metric["relevant_columns"],
        alias=metric["alias"]
    )


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

    logger.info(f'table_column_dict 1：{table_column_dict}')


    # # 补充：相关表的主外键字段信息
    for table_id,column_list in table_column_dict.items():
        # 去查询meta库当前表的主外键字段信息
        key_column_infos: list[ColumnInfoMySQL] = await meta_mysql_repo.get_key_column_infos_by_table_id(table_id)
        for key_column_info in key_column_infos:
            # 将主外键的字段信息转成ColumnInfoQdrant对象
            key_column_info_qdrant = _convert_column_info_mysql_to_qdrant(key_column_info)
            if key_column_info.id not in column_infos_dict:
                # 当前表的主外键字段的id如果不在column_infos_dict中
                # 那么，肯定不在table_column_dict当中
                # 因为，table_column_dict是根据column_infos_dict生成的
                table_column_dict[table_id].append(key_column_info_qdrant)

        # 生成TableInfoState对象列表:
        # 1.根据当前表的id查询meta库获取表的信息
        table_info: TableInfoMySQL = await meta_mysql_repo.get_table_info_by_id(table_id)
        # 2.创建ColumnInfoState对象列表
        columns: list[ColumnInfoState] = [_convert_column_info_qdrant_to_state(column) for column in column_list]
        # 3.TableInfoState对象
        table_info_state: TableInfoState = TableInfoState(
            name=table_info.name,
            role=table_info.role,
            description=table_info.description,
            columns=columns
        )
        table_infos.append(table_info_state)


    # 创建MetricInfoState对象列表:
    metric_infos: list[MetricInfoState] = [_convert_metric_info_qdrant_to_state(metric) for metric in recall_metrics]

    logger.info(f'合并召回信息：{table_infos}--{metric_infos}')

    # 更新状态数据
    return {"table_infos": table_infos, "metric_infos": metric_infos}
