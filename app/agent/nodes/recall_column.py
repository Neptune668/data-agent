from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext
from app.agent.llm import llm
from app.agent.state import DataAgentState
from app.core.log import logger
from app.models.qdrant.column_info_qdrant import ColumnInfoQdrant
from app.prompt.prompt_loader import load_prompt


# 节点：召回字段信息
async def recall_column(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    # 输出给前端的数据（前后端约定好的格式）
    runtime.stream_writer({"stage": "召回字段信息"})

    query = state['query']
    keywords = state['keywords']
    embedding_client = runtime.context["embedding_client"]
    column_qdrant_repo = runtime.context["column_qdrant_repo"]

    # 1.用大模型对query进行分词，与jieba的分词进行合并（去重）
    # 2.用合并后的分词去做召回
    # 3.对每一个分词进行向量化，然后查询qdrant库
    # 4.得到 list[ColumnInfoQdrant]

    # 提示词模板
    prompt = PromptTemplate(
       template=load_prompt('extend_keywords_for_column_recall'),
       input_variables=["query"]
    )

    # 输出解析器
    output_parser = JsonOutputParser()

    # 构建langchain处理链
    chain = prompt | llm | output_parser

    # 执行langchain处理链获取结果
    result = await chain.ainvoke({"query": query})
    logger.info(f'recall_column llm keywords: {result}')

    # 合并关键字
    keywords = list(set(keywords+result))
    logger.info(f'recall_column 合并关键字: {keywords}')

    # 保存所有召回字段信息的字典（去重）{column_id: ColumnInfoQdrant}
    recall_columns_dict: dict[str, ColumnInfoQdrant] = {}

    # 遍历keywords
    for keyword in keywords:
        # 对每一个分词进行向量化
        vector = await embedding_client.aembed_query(keyword)

        # 然后查询qdrant库，获取字段信息列表
        payloads: list[ColumnInfoQdrant] = await column_qdrant_repo.search(vector)

        # 遍历去重保存
        for payload in payloads:
            column_id = payload['id']
            if column_id not in recall_columns_dict:
                recall_columns_dict[column_id] = payload

    # 将recall_columns_dict字典转成列表
    recall_columns: list[ColumnInfoQdrant] = list(recall_columns_dict.values())

    logger.info(f'召回字段信息：{recall_columns}')
    # 更新状态数据
    return {"recall_columns": recall_columns}
