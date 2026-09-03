from langchain_huggingface import HuggingFaceEndpointEmbeddings

from app.conf.app_config import EmbeddingConfig, app_config


# embedding客户端管理
class EmbeddingClientManager:
    def __init__(self, config: EmbeddingConfig):
        self.config = config
        self.client: HuggingFaceEndpointEmbeddings | None = None

    def _get_url(self):
        return f'http://{self.config.host}:{self.config.port}'

    def init(self):
        self.client = HuggingFaceEndpointEmbeddings(model=self._get_url())

    # embedding客户端不需要关闭

# 创建embedding客户端管理器
embedding_client_manager = EmbeddingClientManager(app_config.embedding)

# 测试
if __name__ == '__main__':
    # 初始化客户端
    embedding_client_manager.init()
    # 获取客户端
    client = embedding_client_manager.client

    # 对指定文本进行向量化
    text = "你好，世界！"
    vector = client.embed_query(text)
    # print(vector) # [...]
    print(len(vector)) # 1024维度