"""校验 SQL 节点。"""

from langgraph.runtime import Runtime

from app.agent.context import Context
from app.agent.state import State
from app.core.log import logger


def validate_sql(state: State, runtime: Runtime[Context]) -> dict:
    """校验生成的 SQL 是否合法。"""
    logger.info('节点 validate_sql 执行')
    runtime.stream_writer({"stage": "校验SQL"})

    # TODO: 实际校验 SQL 语法/语义
    sql = state.get("sql", "")
    sql_valid = bool(sql and sql.strip())

    return {"sql_valid": sql_valid}
