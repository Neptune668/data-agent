import yaml
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext
from app.agent.llm import llm
from app.agent.state import DataAgentState
from app.core.log import logger
from app.prompt.prompt_loader import load_prompt


# 节点：过滤指标信息
async def filter_metric(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    # 输出给前端的数据（前后端约定好的格式）
    runtime.stream_writer({"stage": "过滤指标信息"})

    query = state["query"]
    metric_infos = state["metric_infos"]

    # 提示词模板
    prompt = PromptTemplate(
        template=load_prompt('filter_metric_info'),
        input_variables=["query", "metric_infos"]
    )

    # 输出解析器
    output_parser = JsonOutputParser()

    # 构建langchain处理链
    chain = prompt | llm | output_parser

    # 执行langchain处理链获取结果
    # 1.数据转成json字符串传给大模型
    # result = await chain.ainvoke({"query": query,"metric_infos": metric_infos})
    # 2.数据转成yaml字符串传给大模型（节约token）
    result = await chain.ainvoke({
        "query": query,
        "metric_infos": yaml.dump(metric_infos, allow_unicode=True, sort_keys=False)
    })

    logger.info(f'metric_infos llm: {result}')

    # 遍历metric_infos，判断不在result中的指标删除
    for metric_info in metric_infos[:]:
        if metric_info["name"] not in result:
            metric_infos.remove(metric_info)

    logger.info(f'过滤指标信息：{metric_infos}')

    # 更新状态数据
    return {"metric_infos": metric_infos}
