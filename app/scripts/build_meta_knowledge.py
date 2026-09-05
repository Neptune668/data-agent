import asyncio

from app.clients.embedding_client_manager import embedding_client_manager
from app.clients.es_client_manager import es_client_manager
from app.clients.mysql_client_manager import dw_mysql_client_manager, meta_mysql_client_manager
from app.clients.qdrant_client_manager import qdrant_client_manager
from app.conf.meta_config import meta_config
from app.core.log import logger
from app.repositories.es.value_es_repository import ValueEsRepository
from app.repositories.mysql.dw_mysql_repository import DWMySQLRepository
from app.repositories.mysql.meta_mysql_repository import MetaMySQLRepository
from app.repositories.qdrant.column_qdrant_repository import ColumnQdrantRepository
from app.repositories.qdrant.metric_qdrant_repository import MetricQdrantRepository
from app.services.meta_knowledge_service import MetaKnowledgeService


async def start_build():
    logger.info('构建元数据知识库 开始')

    # 初始化客户端
    es_client_manager.init()
    qdrant_client_manager.init()
    dw_mysql_client_manager.init()
    meta_mysql_client_manager.init()
    embedding_client_manager.init()

    # 构建元数据知识库，成功提交事务，失败回滚事务
    try:
        # 调用meta_knowledge_service.py中的build()方法构建业务
        async with (dw_mysql_client_manager.session_factory() as dw_session,
                    meta_mysql_client_manager.session_factory() as meta_session):
            service = MetaKnowledgeService(
                value_es_repo=ValueEsRepository(es_client_manager.client),
                dw_mysql_repo=DWMySQLRepository(dw_session),
                meta_mysql_repo=MetaMySQLRepository(meta_session),
                column_qdrant_repo=ColumnQdrantRepository(qdrant_client_manager.client),
                Metric_qdrant_repo=MetricQdrantRepository(qdrant_client_manager.client),
                embedding_client= embedding_client_manager.client
            )
            # 构建业务
            await service.build(meta_config)

            # 成功，提交事务
            await dw_session.commit()
            await meta_session.commit()

        logger.info('构建元数据知识库 完成')
    except Exception as e:
        logger.error(f'构建元数据知识库 失败: {str(e)}')
        # 失败，回滚事务
        await dw_session.rollback()
        await meta_session.rollback()
        raise e # 在控制台抛出错误，方便调试
    finally:
        # 关闭客户端
        await es_client_manager.close()
        await qdrant_client_manager.close()
        await dw_mysql_client_manager.close()
        await meta_mysql_client_manager.close()

if __name__ == '__main__':
    asyncio.run(start_build())
