"""过滤表格信息节点。"""

from langgraph.runtime import Runtime

from app.agent.context import Context
from app.agent.state import State
from app.core.log import logger


def filter_table(state: State, runtime: Runtime[Context]) -> dict:
    """从召回结果中过滤出与查询相关的表信息。"""
    logger.info('节点 filter_table 执行')
    runtime.stream_writer({"stage": "过滤表格信息"})

    # TODO: 使用 LLM 过滤不相关的表信息
    filtered_tables: list = []

    return {"filtered_tables": filtered_tables}
