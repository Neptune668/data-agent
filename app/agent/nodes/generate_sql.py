"""生成 SQL 节点。"""

from langgraph.runtime import Runtime

from app.agent.context import Context
from app.agent.state import State
from app.core.log import logger


def generate_sql(state: State, runtime: Runtime[Context]) -> dict:
    """基于查询与上下文生成 SQL。"""
    logger.info('节点 generate_sql 执行')
    runtime.stream_writer({"stage": "生成SQL"})

    # TODO: 使用 LLM 基于 state['context'] 生成 SQL
    sql: str = ""

    return {"sql": sql}
