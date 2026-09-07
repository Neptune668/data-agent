"""关键词抽取节点。"""

from langgraph.runtime import Runtime

from app.agent.context import Context
from app.agent.state import State
from app.core.log import logger


def extract_keyword(state: State, runtime: Runtime[Context]) -> dict:
    """从用户查询中抽取关键词，用于后续召回。"""
    logger.info('节点 extract_keyword 执行')
    runtime.stream_writer({"stage": "抽取关键词"})

    # TODO: 调用 LLM 从 state['query'] 中抽取关键词
    keywords: list[str] = []

    return {"keywords": keywords}
