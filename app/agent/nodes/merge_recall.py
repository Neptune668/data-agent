"""合并召回信息节点。"""

from langgraph.runtime import Runtime

from app.agent.context import Context
from app.agent.state import State
from app.core.log import logger


def merge_recall(state: State, runtime: Runtime[Context]) -> dict:
    """合并字段/指标/取值三类召回结果。"""
    logger.info('节点 merge_recall 执行')
    runtime.stream_writer({"stage": "合并召回信息"})

    # TODO: 合并 recalled_columns/recalled_metrics/recalled_values
    recall_result: dict = {}

    return {"recall_result": recall_result}
