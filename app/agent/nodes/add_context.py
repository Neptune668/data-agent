"""添加额外上下文信息节点。"""

from langgraph.runtime import Runtime

from app.agent.context import Context
from app.agent.state import State
from app.core.log import logger


def add_context(state: State, runtime: Runtime[Context]) -> dict:
    """组装字段/指标/表等上下文，供 SQL 生成使用。"""
    logger.info('节点 add_context 执行')
    runtime.stream_writer({"stage": "添加上下文信息"})

    # TODO: 根据过滤后的表/指标信息组装上下文
    context: str = ""

    return {"context": context}
