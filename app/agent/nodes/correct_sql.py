"""校正 SQL 节点。"""

from langgraph.runtime import Runtime

from app.agent.context import Context
from app.agent.state import State
from app.core.log import logger


def correct_sql(state: State, runtime: Runtime[Context]) -> dict:
    """校正校验未通过的 SQL。"""
    logger.info('节点 correct_sql 执行')
    runtime.stream_writer({"stage": "校正SQL"})

    # TODO: 使用 LLM 校正错误的 SQL
    sql = state.get("sql", "")

    return {"sql": sql}
