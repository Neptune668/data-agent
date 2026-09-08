from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState
from app.core.log import logger


# 节点：校验SQL
async def validate_sql(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    # 输出给前端的数据（前后端约定好的格式）
    runtime.stream_writer({"stage": "校验SQL"})

    sql = state["sql"]
    dw_mysql_repo = runtime.context["dw_mysql_repo"]

    try:
        # 校验SQL
        await dw_mysql_repo.validate_sql(sql)

        # 没有异常，说明校验成功
        logger.info(f'校验SQL成功：{sql}')

        return {"error": None}  # 走执行SQL流程
    except Exception as e:
        # 有异常，校验失败
        logger.error(f'校验SQL失败：{sql}，错误信息：{str(e)}')
        return {"error": str(e)}  # 走校正SQL流程
