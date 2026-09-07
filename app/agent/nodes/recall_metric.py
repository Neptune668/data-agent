from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext
from app.agent.llm import llm
from app.agent.state import DataAgentState
from app.core.log import logger
from app.models.qdrant.column_info_qdrant import ColumnInfoQdrant
from app.models.qdrant.metric_info_qdrant import MetricInfoQdrant
from app.prompt.prompt_loader import load_prompt


# 节点：召回指标信息
async def recall_metric(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    # 输出给前端的数据（前后端约定好的格式）
    runtime.stream_writer({"stage": "召回指标信息"})

    query = state['query']
    keywords = state['keywords']
    embedding_client = runtime.context["embedding_client"]
    metric_qdrant_repo = runtime.context["metric_qdrant_repo"]

    # 1.用大模型对query进行分词，与jieba的分词进行合并（去重）
    # 2.用合并后的分词去做召回
    # 3.对每一个分词进行向量化，然后查询qdrant库
    # 4.得到 list[MetricInfoQdrant]

    # 提示词模板
    prompt = PromptTemplate(
       template=load_prompt('extend_keywords_for_metric_recall'),
       input_variables=["query"]
    )

    # 输出解析器
    output_parser = JsonOutputParser()

    # 构建langchain处理链
    chain = prompt | llm | output_parser

    # 执行langchain处理链获取结果
    result = await chain.ainvoke({"query": query})
    logger.info(f'recall_metric llm keywords: {result}')

    # 合并关键字
    keywords = list(set(keywords+result))
    logger.info(f'recall_column 合并关键字: {keywords}')

    # 保存所有召回指标信息的字典（去重）{column_id: MetricInfoQdrant}
    recall_metrics_dict: dict[str, MetricInfoQdrant] = {}

    # 遍历keywords
    for keyword in keywords:
        # 对每一个分词进行向量化
        vector = await embedding_client.aembed_query(keyword)

        # 然后查询qdrant库，获取字段信息列表
        payloads: list[MetricInfoQdrant] = await metric_qdrant_repo.search(vector)

        # 遍历去重保存
        for payload in payloads:
            column_id = payload['id']
            if column_id not in recall_metrics_dict:
                recall_metrics_dict[column_id] = payload

    # 将recall_metrics_dict字典转成列表
    recall_metrics: list[MetricInfoQdrant] = list(recall_metrics_dict.values())

    logger.info(f'召回指标信息：{recall_metrics}')
    # 更新状态数据
    return {"recall_metrics": recall_metrics}