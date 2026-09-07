"""召回字段信息节点。"""

from langgraph.runtime import Runtime

from app.agent.context import Context
from app.agent.state import State
from app.core.log import logger


def recall_column(state: State, runtime: Runtime[Context]) -> dict:
    """基于关键词从向量库召回相关字段信息。"""
    logger.info('节点 recall_column 执行')
    runtime.stream_writer({"stage": "召回字段信息"})

    # TODO: 使用 runtime.context['column_qdrant_repo'] 召回字段
    recalled_columns: list = []

    return {"recalled_columns": recalled_columns}
