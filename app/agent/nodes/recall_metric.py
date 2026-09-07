"""召回指标信息节点。"""

from langgraph.runtime import Runtime

from app.agent.context import Context
from app.agent.state import State
from app.core.log import logger


def recall_metric(state: State, runtime: Runtime[Context]) -> dict:
    """基于关键词从向量库召回相关指标信息。"""
    logger.info('节点 recall_metric 执行')
    runtime.stream_writer({"stage": "召回指标信息"})

    # TODO: 使用 runtime.context['metric_qdrant_repo'] 召回指标
    recalled_metrics: list = []

    return {"recalled_metrics": recalled_metrics}
