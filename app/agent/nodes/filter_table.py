import yaml
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext
from app.agent.llm import llm
from app.agent.state import DataAgentState
from app.core.log import logger
from app.prompt.prompt_loader import load_prompt


# 节点：过滤表信息
async def filter_table(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    # 输出给前端的数据（前后端约定好的格式）
    runtime.stream_writer({"stage": "过滤表信息"})

    query = state["query"]
    table_infos = state["table_infos"]

    # 提示词模板
    prompt = PromptTemplate(
        template=load_prompt('filter_table_info'),
        input_variables=["query","table_infos"]
    )

    # 输出解析器
    output_parser = JsonOutputParser()

    # 构建langchain处理链
    chain = prompt | llm | output_parser

    # 执行langchain处理链获取结果
    # 1.数据转成json字符串传给大模型
    # result = await chain.ainvoke({"query": query,"table_infos": table_infos})
    # 2.数据转成yaml字符串传给大模型（节约token）
    result = await chain.ainvoke({
        "query": query,
        "table_infos": yaml.dump(table_infos,allow_unicode=True,sort_keys=False)
    })

    logger.info(f'filter_table llm: {result}')

    # 遍历浅拷贝出来的列表
    # table_infos_copy = table_infos[:]
    for table_info in table_infos[:]:
        if table_info["name"] not in result:
            # 过滤表
            table_infos.remove(table_info) # 删除表
        else:
            # 过滤表对应的字段
            columns = table_info["columns"]
            for column in columns[:]:
                if column["name"] not in result[table_info["name"]]:
                    columns.remove(column) # 删除字段

    logger.info(f'过滤表信息: {table_infos}')

    # 更新状态数据
    return {"table_infos": table_infos}