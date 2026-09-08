import asyncio

from langgraph.constants import START, END
from langgraph.graph import StateGraph

from app.agent.context import DataAgentContext
from app.agent.nodes.add_context import add_context
from app.agent.nodes.correct_sql import correct_sql
from app.agent.nodes.execute_sql import execute_sql
from app.agent.nodes.extract_keyword import extract_keyword
from app.agent.nodes.filter_metric import filter_metric
from app.agent.nodes.filter_table import filter_table
from app.agent.nodes.generate_sql import generate_sql
from app.agent.nodes.merge_recall import merge_recall
from app.agent.nodes.recall_column import recall_column
from app.agent.nodes.recall_metric import recall_metric
from app.agent.nodes.recall_value import recall_value
from app.agent.nodes.validate_sql import validate_sql
from app.agent.state import DataAgentState
from app.clients.embedding_client_manager import embedding_client_manager
from app.clients.es_client_manager import es_client_manager
from app.clients.mysql_client_manager import dw_mysql_client_manager, meta_mysql_client_manager
from app.clients.qdrant_client_manager import qdrant_client_manager
from app.core.log import logger
from app.repositories.es.value_es_repository import ValueEsRepository
from app.repositories.mysql.dw_mysql_repository import DWMySQLRepository
from app.repositories.mysql.meta_mysql_repository import MetaMySQLRepository
from app.repositories.qdrant.column_qdrant_repository import ColumnQdrantRepository
from app.repositories.qdrant.metric_qdrant_repository import MetricQdrantRepository

# 创建图构建器
graph_builder = StateGraph(
    state_schema=DataAgentState,
    context_schema=DataAgentContext
)

# 添加节点
graph_builder.add_node('extract_keyword', extract_keyword)
graph_builder.add_node('recall_column', recall_column)
graph_builder.add_node('recall_metric', recall_metric)
graph_builder.add_node('recall_value', recall_value)
graph_builder.add_node('merge_recall', merge_recall)
graph_builder.add_node('filter_table', filter_table)
graph_builder.add_node('filter_metric', filter_metric)
graph_builder.add_node('add_context', add_context)
graph_builder.add_node('generate_sql', generate_sql)
graph_builder.add_node('validate_sql', validate_sql)
graph_builder.add_node('correct_sql', correct_sql)
graph_builder.add_node('execute_sql', execute_sql)

# 添加边
graph_builder.add_edge(START, 'extract_keyword')
graph_builder.add_edge('extract_keyword', 'recall_column')
graph_builder.add_edge('extract_keyword', 'recall_metric')
graph_builder.add_edge('extract_keyword', 'recall_value')
graph_builder.add_edge('recall_column', 'merge_recall')
graph_builder.add_edge('recall_metric', 'merge_recall')
graph_builder.add_edge('recall_value', 'merge_recall')
graph_builder.add_edge('merge_recall', 'filter_table')
graph_builder.add_edge('merge_recall', 'filter_metric')
graph_builder.add_edge('filter_metric', 'add_context')
graph_builder.add_edge('filter_table', 'add_context')
graph_builder.add_edge('add_context', 'generate_sql')
graph_builder.add_edge('generate_sql', 'validate_sql')

# 添加条件边
graph_builder.add_conditional_edges(
    'validate_sql',  # 根据这个节点的返回值做判断
    lambda state: 'execute_sql' if state.get('error') is None else 'correct_sql',  # 判断条件
    {'execute_sql': 'execute_sql', 'correct_sql': 'correct_sql'}  # 根据条件跳转的节点
)

# 添加边
graph_builder.add_edge('correct_sql', 'execute_sql')
graph_builder.add_edge('execute_sql', END)

# 编译图
graph = graph_builder.compile()

# 查看图结构
# print( graph.get_graph().draw_mermaid() )

if __name__ == '__main__':
    async def test():
        # 初始化客户端
        embedding_client_manager.init()
        es_client_manager.init()
        qdrant_client_manager.init()
        dw_mysql_client_manager.init()
        meta_mysql_client_manager.init()

        try:
            async with dw_mysql_client_manager.session_factory() as dw_session, meta_mysql_client_manager.session_factory() as meta_session:
                # 创建上下文对象
                context = DataAgentContext(
                    value_es_repo=ValueEsRepository(es_client_manager.client),
                    dw_mysql_repo=DWMySQLRepository(dw_session),
                    meta_mysql_repo=MetaMySQLRepository(meta_session),
                    column_qdrant_repo=ColumnQdrantRepository(qdrant_client_manager.client),
                    metric_qdrant_repo=MetricQdrantRepository(qdrant_client_manager.client),
                    embedding_client=embedding_client_manager.client
                )

                # 创建状态对象
                state = DataAgentState(query='统计3月销售总额最高的3个产品')
                # state = DataAgentState(query='统计华北地区3月销售总额')

                # 异步流式执行图
                async for chunk in graph.astream(input=state, context=context, stream_mode='custom'):
                    print(chunk)
        except Exception as e:
            logger.info(f'构建失败：{str(e)}')
            raise e
        finally:
            await qdrant_client_manager.close()
            await es_client_manager.close()
            await dw_mysql_client_manager.close()
            await meta_mysql_client_manager.close()


    asyncio.run(test())
