"""执行 SQL 节点。"""

from langgraph.runtime import Runtime

from app.agent.context import Context
from app.agent.state import State
from app.core.log import logger


def execute_sql(state: State, runtime: Runtime[Context]) -> dict:
    """执行 SQL 并返回结果。"""
    logger.info('节点 execute_sql 执行')
    runtime.stream_writer({"stage": "执行SQL"})

    # TODO: 使用 runtime.context['dw_mysql_repo'] 执行 SQL
    sql_result: str = ""

    return {"sql_result": sql_result}
