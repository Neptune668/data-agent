from datetime import datetime

from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState, DateInfoState, DBInfoState
from app.core.log import logger


# 节点：添加额外信息
async def add_context(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    # 输出给前端的数据（前后端约定好的格式）
    runtime.stream_writer({"stage": "添加额外信息"})

    dw_mysql_repo = runtime.context['dw_mysql_repo']

    # 获取日期时间
    # today: 2026-09-08 11:50:21.557108
    today = datetime.today()
    date = today.strftime("%Y-%m-%d")
    weekday = today.strftime("%A")
    # quarter=f"Q{(today.month-1)//3+1}"
    quarter=f"Q{(today.month+2)//3}"

    # 创建DateInfoState对象
    date_info = DateInfoState(date=date, weekday=weekday, quarter=quarter)

    # {"dialect": '', "version": ''}
    db_info_dict: dict = await dw_mysql_repo.get_db_info()
    # 创建DBInfoState对象
    db_info = DBInfoState(**db_info_dict)

    logger.info(f'添加额外信息: {date_info}--{db_info}')

    # 更新状态数据
    return {"date_info": date_info, "db_info": db_info}