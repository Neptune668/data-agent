import yaml
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext
from app.agent.llm import llm
from app.agent.state import DataAgentState
from app.core.log import logger
from app.prompt.prompt_loader import load_prompt


# 节点：校正SQL
async def correct_sql(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    # 输出给前端的数据（前后端约定好的格式）
    runtime.stream_writer({"stage": "校正SQL"})

    query = state["query"]
    table_infos = state["table_infos"]
    metric_infos = state["metric_infos"]
    date_info = state["date_info"]
    db_info = state["db_info"]
    sql = state["sql"]
    error = state["error"]

    # 提示词模板
    prompt = PromptTemplate(
        template=load_prompt('correct_sql'),
        input_variables=["query", "table_infos", "metric_infos", "date_info", "db_info", "sql", "error"]
    )

    # 输出解析器
    output_parser = StrOutputParser()

    # 构建langchain处理链
    chain = prompt | llm | output_parser

    # 执行langchain处理链获取结果
    sql = await chain.ainvoke({
        "query": query,
        "table_infos": yaml.dump(table_infos, allow_unicode=True, sort_keys=False),
        "metric_infos": yaml.dump(metric_infos, allow_unicode=True, sort_keys=False),
        "date_info": yaml.dump(date_info, allow_unicode=True, sort_keys=False),
        "db_info": yaml.dump(db_info, allow_unicode=True, sort_keys=False),
        "sql": sql,
        "error": error
    })

    logger.info(f"校正SQL：{sql}")

    # 更新状态数据
    return {"sql": sql}