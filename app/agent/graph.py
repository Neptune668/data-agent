"""构建 langgraph 图。"""

from langgraph.constants import END, START
from langgraph.graph import StateGraph

from app.agent.context import Context
from app.agent.nodes.add_context import add_context
from app.agent.nodes.correct_sql import correct_sql
from app.agent.nodes.execute_sql import execute_sql
from app.agent.nodes.extract_keyword import extract_keyword
from app.agent.nodes.filter_metric import filter_metric
from app.agent.nodes.filter_table import filter_table
from app.agent.nodes.generate_sql import generate_sql
from app.agent.nodes.merge_recall import merge_recall
from app.agent.nodes.recall_column import recall_column
from app.agent.nodes.recall_metric import recall_metric
from app.agent.nodes.recall_value import recall_value
from app.agent.nodes.validate_sql import validate_sql
from app.agent.state import State


def route_after_validate(state: State) -> str:
    """根据 SQL 校验结果路由到下一步。"""
    return "execute_sql" if state.get("sql_valid") else "correct_sql"


# 创建图构建器
graph_builder = StateGraph(state_schema=State, context_schema=Context)

# 添加节点
graph_builder.add_node("extract_keyword", extract_keyword)
graph_builder.add_node("recall_column", recall_column)
graph_builder.add_node("recall_metric", recall_metric)
graph_builder.add_node("recall_value", recall_value)
graph_builder.add_node("merge_recall", merge_recall)
graph_builder.add_node("filter_table", filter_table)
graph_builder.add_node("filter_metric", filter_metric)
graph_builder.add_node("add_context", add_context)
graph_builder.add_node("generate_sql", generate_sql)
graph_builder.add_node("validate_sql", validate_sql)
graph_builder.add_node("correct_sql", correct_sql)
graph_builder.add_node("execute_sql", execute_sql)

# 添加边
graph_builder.add_edge(START, "extract_keyword")

# extract_keyword 扇出到三个召回节点（并行）
graph_builder.add_edge("extract_keyword", "recall_column")
graph_builder.add_edge("extract_keyword", "recall_metric")
graph_builder.add_edge("extract_keyword", "recall_value")

# 三个召回节点扇入到 merge_recall
graph_builder.add_edge("recall_column", "merge_recall")
graph_builder.add_edge("recall_metric", "merge_recall")
graph_builder.add_edge("recall_value", "merge_recall")

# merge_recall 扇出到两个过滤节点（并行）
graph_builder.add_edge("merge_recall", "filter_table")
graph_builder.add_edge("merge_recall", "filter_metric")

# 两个过滤节点扇入到 add_context
graph_builder.add_edge("filter_table", "add_context")
graph_builder.add_edge("filter_metric", "add_context")

# add_context -> generate_sql -> validate_sql
graph_builder.add_edge("add_context", "generate_sql")
graph_builder.add_edge("generate_sql", "validate_sql")

# validate_sql 条件路由：合法 -> execute_sql，非法 -> correct_sql
graph_builder.add_conditional_edges("validate_sql", route_after_validate)

# correct_sql -> execute_sql -> END
graph_builder.add_edge("correct_sql", "execute_sql")
graph_builder.add_edge("execute_sql", END)

# 编译图
graph = graph_builder.compile()
