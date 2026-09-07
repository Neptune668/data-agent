from qdrant_client import AsyncQdrantClient, models

from app.conf.app_config import app_config
from app.models.qdrant.column_info_qdrant import ColumnInfoQdrant


class ColumnQdrantRepository:
    collection_name = 'column_collection'
    def __init__(self, client: AsyncQdrantClient):
        self.client = client

    async def upsert_column_vectors(self, ids: list[str], vectors: list[list[float]], payloads: list[ColumnInfoQdrant]):
        if not await self.client.collection_exists(collection_name=self.collection_name):
            # 创建集合
            await self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=app_config.qdrant.embedding_size,  # 向量维度
                    distance=models.Distance.COSINE  # 向量距离的算法
                )
            )

        # 添加数据/修改数据
        # 实际项目中一次性插入所有向量，很耗时甚至崩溃
        # await self.client.upsert(
        #     collection_name=self.collection_name,
        #     points=[
        #         models.PointStruct(
        #             id=ids[i],  # 数据id
        #             vector=vectors[i],  # 向量数据
        #             payload=payloads[i] # 向量的相关数据
        #         )
        #         for i in range(len(ids))
        #     ]
        # )

        # 分批插入向量
        batch_size = 10
        for i in range(0, len(ids), batch_size):
            # 获取分批的数据
            batch_ids = ids[i:i+batch_size]
            batch_vectors = vectors[i:i+batch_size]
            batch_payloads = payloads[i:i+batch_size]
            # 插入分批数据
            await self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=batch_ids[i],  # 数据id
                        vector=batch_vectors[i],  # 向量数据
                        payload=batch_payloads[i] # 向量的相关数据
                    )
                    for i in range(len(batch_ids))
                ]
            )


    async def search(self, vector: list[list[float]])->list[ColumnInfoQdrant]:
        result = await self.client.query_points(
            collection_name=self.collection_name,
            query=vector,
            score_threshold=0.6
        )
        # return [ponit.payload for ponit in result.points]
        return [ColumnInfoQdrant(**ponit.payload) for ponit in result.points]