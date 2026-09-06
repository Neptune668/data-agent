import asyncio

from elasticsearch import AsyncElasticsearch

from app.conf.app_config import ESConfig, app_config


class EsClientManager:
    # 初始化实例属性
    def __init__(self, config: ESConfig):
        self.config = config
        self.client: AsyncElasticsearch | None = None

    # 获取连接的urlz
    def _get_url(self):
        return f'http://{self.config.host}:{self.config.port}'

    # 初始化客户端
    def init(self):
        self.client = AsyncElasticsearch(self._get_url())

    # 关闭客户端
    async def close(self):
        await self.client.close()


# 创建ES客户端管理器
es_client_manager = EsClientManager(app_config.es)

# 测试
if __name__ == '__main__':
    async def test():
        # 初始化客户端
        es_client_manager.init()
        # 获取客户端
        client = es_client_manager.client

        # 如果索引存在，则删除索引
        if await client.indices.exists(index='test_index'):
            await client.indices.delete(index='test_index')

        # 创建index索引
        await client.indices.create(
            index='test_index',
            mappings={
                "dynamic": False,  # 关闭动态映射
                "properties": {
                    "name": {
                        "type": "text"
                    },
                    "author": {
                        "type": "text"
                    },
                    "release_date": {
                        "type": "date",
                        "format": "yyyy-MM-dd"
                    },
                    "page_count": {
                        "type": "integer"
                    }
                }
            }
        )

        # 添加多条文档数据
        await client.bulk(
            operations=[
                {
                    "index": {
                        "_index": "test_index"
                    }
                },
                {
                    "name": "Revelation Space",
                    "author": "Alastair Reynolds",
                    "release_date": "2000-03-15",
                    "page_count": 585
                },
                {
                    "index": {
                        "_index": "test_index"
                    }
                },
                {
                    "name": "1984",
                    "author": "George Orwell",
                    "release_date": "1985-06-01",
                    "page_count": 328
                },
                {
                    "index": {
                        "_index": "test_index"
                    }
                },
                {
                    "name": "Fahrenheit 451",
                    "author": "Ray Bradbury",
                    "release_date": "1953-10-15",
                    "page_count": 227
                },
                {
                    "index": {
                        "_index": "test_index"
                    }
                },
                {
                    "name": "Brave New World",
                    "author": "Aldous Huxley",
                    "release_date": "1932-06-01",
                    "page_count": 268
                },
                {
                    "index": {
                        "_index": "test_index"
                    }
                },
                {
                    "name": "The Handmaids Tale",
                    "author": "Margaret Atwood",
                    "release_date": "1985-06-01",
                    "page_count": 311
                }
            ],
            # refresh=True # 立即刷新数据（每插入一条文档，立即刷新一次）
        )

        # 1.执行插入文档后，并不会马上写入ES，数据在缓冲区，需要1秒后才写入数据
        # await asyncio.sleep(1)

        # 2.设置立即刷新数据 refresh = True

        # 3.手动刷新数据
        await client.indices.refresh(index='test_index')

        # 查询数据
        result = await client.search(
            index="test_index",
            query={  # 设置搜索条件
                "match": {  # 设置要搜索的键和值
                    "name": "brave"
                }
            },
        )
        print(result)  # <coroutine object AsyncElasticsearch.search at 0x0000021C64EE6AA0>
        print(result['hits']['hits'][0])
        print(result['hits']['hits'][0]['_source'])  # 搜索的数据

        # 关闭客户端
        await es_client_manager.close()


    asyncio.run(test())
