"""
LangGraph 重点：

状态图：StateGraph的实例
节点：实现特定功能的函数
边：两个节点之间的连线
状态：包含多个可变数据的对象，在图的各个节点上流传

节点函数的参数：
    1. state 包含多个可变数据的对象
    2. runtime 运行时对象，包含以下内容：
        stream_writer: 流式输出，向调用者输出自定义数据
        store: 数据存储，实现跨会话长期存储
        context: 上下文对象，包含指定的固定数据或依赖
    3. config：保存配置的对象(不常用)，比如执行时指定的 thread_id
"""
import asyncio
from typing import TypedDict

from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.runtime import Runtime

from app.repositories.mysql.dw_mysql_repository import DWMySQLRepository
from app.repositories.mysql.meta_mysql_repository import MetaMySQLRepository


# 通常保存可变的数据
class MyState(TypedDict):
    query: str
    sql: str

# 通常保存不可变数据(依赖)
class MyContext(TypedDict):
    dw_mysql_repo: DWMySQLRepository
    meta_mysql_repo: MetaMySQLRepository
    db_name: str

# 节点1
def extract_keyword(state: MyState,runtime: Runtime[MyContext]):
    print('节点extract_keyword执行')
    print('state=',state)

    # 前后端约定好的数据格式：{"stage": "提取关键字"}
    runtime.stream_writer({"stage": "提取关键字"})

    sql = 'select * from table where id = 1'

    # state在节点中应该是只读的，不要这样修改数据
    # state['sql'] = sql

    # 在graph内部会自动合并state  reducer
    return {'sql': sql}

# 节点2
def test_node(state: MyState,runtime: Runtime[MyContext]):
    runtime.stream_writer({"stage": "测试内容"})

    print('节点test_node执行')
    print('state=',state)

    return {"query": "我是爸爸"}

# 创建图构建器
graph_builder = StateGraph(state_schema=MyState, context_schema=MyContext)


# 添加节点
graph_builder.add_node('extract_keyword', extract_keyword)
graph_builder.add_node('test_node', test_node)

# 添加边
graph_builder.add_edge(START,'extract_keyword')
graph_builder.add_edge('extract_keyword','test_node')
graph_builder.add_edge('test_node',END)

# 编译图
graph = graph_builder.compile()

if __name__ == '__main__':
    async def test():
       state = MyState(query='你是谁')
       context = MyContext(db_name='xxx')
       """
       stream_mode:
           updates: 外部得到的是节点返回的更新
           values: 外部得到更新合并后的state值
           custom: 外部得到runtime.stream_writer输出的内容
       """

       async for chunk in graph.astream(input=state, context=context, stream_mode='custom'):
           print('------------------', chunk)

    asyncio.run(test())