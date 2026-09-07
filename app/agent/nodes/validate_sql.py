from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState


# 节点：校验SQL
def validate_sql(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    # 输出给前端的数据（前后端约定好的格式）
    runtime.stream_writer({"stage": "校验SQL"})

    # 更新状态数据
    # 校验成功error为None，校验失败为错误信息
    return {"error": None} # 走执行SQL流程
    # return {"error": "has error"} # 走校正SQL流程
