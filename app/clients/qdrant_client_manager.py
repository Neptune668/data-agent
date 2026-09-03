import asyncio

from qdrant_client import AsyncQdrantClient, models

from app.conf.app_config import QdrantConfig, app_config


# qdrant客户端管理
class QdrantClientManager:
    # 初始化实例属性
    def __init__(self, config: QdrantConfig):
        self.config = config
        self.client: AsyncQdrantClient | None = None

    # 获取连接的url
    def _get_url(self):
        return "http://{}:{}".format(self.config.host, self.config.port)

    # 初始化客户端
    def init(self):
        self.client = AsyncQdrantClient(self._get_url())

    # 关闭客户端
    async def close(self):
        await self.client.close()

# 创建qdrant客户端管理实例
qdrant_client_manager: QdrantClientManager = QdrantClientManager(app_config.qdrant)

# 测试
if __name__ == '__main__':
    async def test():
        # 初始化客户端
        qdrant_client_manager.init()
        # 获取客户端
        client = qdrant_client_manager.client

        # 判断集合是否已存在
        if await client.collection_exists(collection_name="test_collection"):
            # 删除集合（测试用）
            await client.delete_collection(collection_name="test_collection")
        # 创建集合
        await client.create_collection(
            collection_name="test_collection",
            vectors_config=models.VectorParams(
                size=4, # 向量维度
                distance=models.Distance.COSINE # 向量距离的算法
            )
        )

        # 判断集合是否已存在(生产用)
        # if not await client.collection_exists(collection_name="test_collection"):
        #     # 创建集合
        #     await client.create_collection(
        #         collection_name="test_collection",
        #         vectors_config=models.VectorParams(
        #             size=4,  # 向量维度
        #             distance=models.Distance.COSINE  # 向量距离的算法
        #         )
        #     )

        # 添加数据/修改数据
        await client.upsert(
            collection_name="test_collection",
            points=[
                models.PointStruct(
                    id=1, # 数据id
                    vector=[1.0, 0.2, 0.3, 0.4], # 向量数据
                    payload={"name": "test1"} # 向量的相关数据
                ),
                models.PointStruct(
                    id=2,  # 数据id
                    vector=[1.0, 0.2, 0.3, 0.5],  # 向量数据
                    payload={"name": "test2"}  # 向量的相关数据
                ),
                models.PointStruct(
                    id=3,  # 数据id
                    vector=[1.0, 0.2, -0.3, 0.6],  # 向量数据
                    payload={"name": "test3"}  # 向量的相关数据
                ),
                models.PointStruct(
                    id=4,  # 数据id
                    vector=[1.0, 0.2, 0.3, 0.7],  # 向量数据
                    payload={"name": "test4"}  # 向量的相关数据
                ),
                models.PointStruct(
                    id=5,  # 数据id
                    vector=[1.0, 0.2, 0.3, 0.8],  # 向量数据
                    payload={"name": "test5"}  # 向量的相关数据
                ),
            ]
        )

        # 删除数据
        # result = await client.delete(
        #     collection_name='test_collection',
        #     points_selector=[1,3] # 删除id为1和3的数据
        # )
        # print(result.status) # completed表示删除完成

        # 查询数据
        result = await client.query_points(
            collection_name="test_collection",
            query=[1.0, 0.2, 0.3, 0.4], # 要查询的向量
            limit=3, # 返回3个最相似的向量
            score_threshold=0.6 # 相似度阈值，只返回高于阈值的向量
        )
        print(result)
        print(result.points[0].payload) # {'name': 'test1'}

        # 关闭客户端
        await qdrant_client_manager.close()

    asyncio.run(test())