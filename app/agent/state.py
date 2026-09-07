"""定义 langgraph 状态。"""

from typing import TypedDict


class State(TypedDict, total=False):
    """LangGraph 状态：在各节点间流转的可变数据。

    节点通过返回值更新状态，langgraph 内部会自动合并。
    """
    query: str              # 用户输入的自然语言查询
    keywords: list[str]     # extract_keyword 抽取出的关键词
    recalled_columns: list  # recall_column 召回的字段信息
    recalled_metrics: list  # recall_metric 召回的指标信息
    recalled_values: list   # recall_value 召回的字段取值信息
    recall_result: dict     # merge_recall 合并后的召回结果
    filtered_tables: list   # filter_table 过滤后的表信息
    filtered_metrics: list  # filter_metric 过滤后的指标信息
    context: str            # add_context 组装后的上下文
    sql: str                # generate_sql 生成的 SQL
    sql_valid: bool         # validate_sql 校验结果
    sql_result: str         # execute_sql 执行结果
