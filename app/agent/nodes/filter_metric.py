"""过滤指标信息节点。"""

from langgraph.runtime import Runtime

from app.agent.context import Context
from app.agent.state import State
from app.core.log import logger


def filter_metric(state: State, runtime: Runtime[Context]) -> dict:
    """从召回结果中过滤出与查询相关的指标信息。"""
    logger.info('节点 filter_metric 执行')
    runtime.stream_writer({"stage": "过滤指标信息"})

    # TODO: 使用 LLM 过滤不相关的指标信息
    filtered_metrics: list = []

    return {"filtered_metrics": filtered_metrics}
