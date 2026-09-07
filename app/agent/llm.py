"""初始化大语言模型（DeepSeek）。"""
import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_deepseek import ChatDeepSeek



def create_llm(temperature: float = 0, **kwargs) -> ChatDeepSeek:
    """根据配置创建 DeepSeek 大模型实例。

    Args:
        temperature: 采样温度，默认 0（确定性输出，适合 SQL 生成等任务）。
        **kwargs: 透传给 ChatDeepSeek 的其他参数（如 max_tokens、timeout 等）。

    Returns:
        配置好的 ChatDeepSeek 实例。
    """
    load_dotenv()
    # return ChatDeepSeek(
    #     model=app_config.llm.model_name,
    #     api_key=app_config.llm.api_key,
    #     temperature=temperature,
    #     **kwargs,
    # )
    return init_chat_model(
        model=os.getenv("LLM_MODEL_NAME"),
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_API_URL"),
        model_provider="openai",
        temperature=temperature, **kwargs)

# 全局 LLM 实例，供 langgraph 各节点直接引用
llm = create_llm()
if __name__ == '__main__':
    result = llm.invoke("你是什么模型")
    print(result.content)
