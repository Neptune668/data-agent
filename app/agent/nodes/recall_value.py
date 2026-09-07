"""召回字段取值节点。"""

from langgraph.runtime import Runtime

from app.agent.context import Context
from app.agent.state import State
from app.core.log import logger


def recall_value(state: State, runtime: Runtime[Context]) -> dict:
    """基于关键词从全文索引召回相关字段取值信息。"""
    logger.info('节点 recall_value 执行')
    runtime.stream_writer({"stage": "召回字段取值"})

    # TODO: 使用 runtime.context['value_es_repo'] 召回字段取值
    recalled_values: list = []

    return {"recalled_values": recalled_values}
