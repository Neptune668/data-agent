import jieba.analyse
from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState
from app.core.log import logger


# 节点：提取关键字
def extract_keyword(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    # 输出给前端的数据（前后端约定好的格式）
    runtime.stream_writer({"stage": "提取关键字"})

    query = state["query"]

    # 指定需要的词性
    allow_pos = (
        "n",  # 名词: 数据、服务器、表格
        "nr",  # 人名: 张三、李四
        "ns",  # 地名: 北京、上海
        "nt",  # 机构团体名: 政府、学校、某公司
        "nz",  # 其他专有名词: Unicode、哈希算法、诺贝尔奖
        "v",  # 动词: 运行、开发
        "vn",  # 名动词: 工作、研究
        "a",  # 形容词: 美丽、快速
        "an",  # 名形词: 难度、合法性、复杂度
        "eng",  # 英文
        "i",  # 成语
        "l",  # 常用固定短语
        "TIME",
        "t"
    )

    # 使用jieba进行分词
    result: list = jieba.analyse.extract_tags(query, topK=10, allowPOS=allow_pos)
    # query = '统计3月销售总额最高的3个产品'
    # result = ['销售总额', '统计', '最高', '产品']

    # 分词后并不能完整的保留用户的语义
    # 将query和分词合并，后面让大模型处理
    keywords = list(set(result+[query]))

    logger.info(f"提取关键字: {keywords}")

    # 更新状态数据
    return {"keywords": keywords}
