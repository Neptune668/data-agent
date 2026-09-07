from elasticsearch import AsyncElasticsearch

from app.clients.es_client_manager import es_client_manager
from app.models.es.value_info_es import ValueInfoEs


class ValueEsRepository:
    index_name = 'value_index'
    def __init__(self, client: AsyncElasticsearch):
        self.client = client

    async def insert_values(self, value_infos: list[ValueInfoEs]):
        # 初始化客户端
        es_client_manager.init()
        # 获取客户端
        client = es_client_manager.client

        # 如果索引存在，则删除索引
        if await client.indices.exists(index=self.index_name):
            await client.indices.delete(index=self.index_name)

        # 创建index索引
        await client.indices.create(
            index=self.index_name,
            mappings={
                "dynamic": False,  # 关闭动态映射
                "properties": {
                    "id": {"type": "keyword"},
                    "value": {"type": "text","analyzer":"ik_max_word"},
                    "type": {"type": "keyword"},
                    "column_id": {"type": "keyword"},
                    "column_name": {"type": "keyword"},
                    "table_id": {"type": "keyword"},
                    "table_name": {"type": "keyword"},
                }
            }
        )

        # 添加多条文档数据
        # await client.bulk(
        #     operations=[ # 插入一个文档包含 item1 和 item2
        #         { # item1
        #             "index": {
        #                 "_index": "test_index"
        #             }
        #         },
        #         { # item2 是 ValueInfoEs对象
        #             "name": "Revelation Space",
        #             "author": "Alastair Reynolds",
        #             "release_date": "2000-03-15",
        #             "page_count": 585
        #         }
        #     ]
        # )

        operations = []

        item1 = { # item1
            "index": {
                "_index": self.index_name
            }
        }

        for item2 in value_infos:
            operations.append(item1)
            operations.append(item2)

        # 分批插入文档
        batch_size = 20 # 每次插入10个文档
        for i in range(0, len(operations), batch_size):
            batch_operations = operations[i:i + batch_size]
            await client.bulk(operations=batch_operations)

    async def search(self, keyword: str, threshold:float=0.6,limit:int=10)->list[ValueInfoEs]:
        result = await self.client.search(
            index=self.index_name,
            query={  # 设置搜索条件
                "match": {  # 设置要搜索的键和值
                    "value": keyword
                }
            },
            size=limit,
            min_score=threshold
        )

        return [ValueInfoEs(**hit["_source"]) for hit in result["hits"]["hits"]]

