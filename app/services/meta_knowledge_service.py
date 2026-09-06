from langchain_huggingface import HuggingFaceEndpointEmbeddings

from app.conf.meta_config import MetaConfig, TableConfig, MetricConfig
from app.core.log import logger
from app.models.mysql.column_info_mysql import ColumnInfoMySQL
from app.models.mysql.metric_info_mysql import MetricInfoMySQL
from app.models.mysql.table_info_mysql import TableInfoMySQL
from app.repositories.es.value_es_repository import ValueEsRepository
from app.repositories.mysql.dw_mysql_repository import DWMySQLRepository
from app.repositories.mysql.meta_mysql_repository import MetaMySQLRepository
from app.repositories.qdrant.column_qdrant_repository import ColumnQdrantRepository
from app.repositories.qdrant.metric_qdrant_repository import MetricQdrantRepository


class MetaKnowledgeService:
    def __init__(
            self,
            value_es_repo: ValueEsRepository,
            dw_mysql_repo: DWMySQLRepository,
            meta_mysql_repo: MetaMySQLRepository,
            column_qdrant_repo: ColumnQdrantRepository,
            Metric_qdrant_repo: MetricQdrantRepository,
            embedding_client: HuggingFaceEndpointEmbeddings
    ):
        self.value_es_repo = value_es_repo
        self.dw_mysql_repo = dw_mysql_repo
        self.meta_mysql_repo = meta_mysql_repo
        self.column_qdrant_repo = column_qdrant_repo
        self.Metric_qdrant_repo = Metric_qdrant_repo
        self.embedding_client = embedding_client

    async def build(self, config: MetaConfig):
        logger.info('构建业务 开始')
        """构建业务思路分析：
        1.处理表相关信息数据
            1.1保存表信息到meta库的table_info表中
            1.2保存字段信息到meta库column_info表中
            1.3为字段信息建立向量索引
            1.4为字段取值建立全文索引

        2.处理指标相关信息数据
            2.1保存指标信息到meta库的metric_info表中
            2.2保存指标信息到meta库的column_metric表中
            2.3为指标信息建立向量索引
        """

        # 1.处理表相关信息数据
        if config.tables:
            # 1.1保存表信息到meta库的table_info表中
            column_infos: list[ColumnInfoMySQL] = await self._save_table_info_to_meta(config.tables)
            logger.info('保存表信息到meta库')

            # 1.2保存字段信息到meta库column_info表中
            await self._save_column_info_to_meta(column_infos)
            logger.info('保存字段信息到meta库')

            # 1.3为字段信息建立向量索引
            await self._save_column_info_to_qdrant(column_infos)
            logger.info('为字段信息建立向量索引')

            # 1.4为字段取值建立全文索引
            await self._save_column_value_to_es(column_infos, config.tables)
            logger.info('为字段取值建立全文索引')

        # 2.处理指标相关信息数据
        if config.metrics:
            # 2.1保存指标信息到meta库的metric_info表中
            metric_infos: list[MetricInfoMySQL] = await self._save_metric_info_to_meta(config.metrics)
            logger.info('保存指标信息到meta库1')

            # 2.2保存指标信息到meta库的column_metric表中
            await self._save_column_metric_to_meta(config.metrics)
            logger.info('保存指标信息到meta库2')

            # 2.3为指标信息建立向量索引
            await self._save_metric_info_to_qdrant(metric_infos)
            logger.info('为指标信息建立向量索引')

        logger.info('构建业务 完成')

    async def _save_table_info_to_meta(self, tables: list[TableConfig]) -> list[ColumnInfoMySQL]:
        table_infos: list[TableInfoMySQL] = []
        column_infos: list[ColumnInfoMySQL] = []
        # 遍历表信息
        for table in tables:
            # 创建ORM对象
            table_info = TableInfoMySQL(
                id=table.name,
                name=table.name,
                role=table.role,
                description=table.description
            )
            table_infos.append(table_info)

            # 查询dw库当前table中的所有字段数据类型 -> dict[字段名：字段数据类型]
            column_types: dict = await self.dw_mysql_repo.get_column_types(table.name)

            # 遍历当前table的字段信息，构建column_infos
            for column_info in table.columns:
                # 查询dw库取出当前表指定字段的前8条数据
                column_values: list = await self.dw_mysql_repo.get_column_values(table.name, column_info.name, 8)

                # 创建ORM对象
                column_info_mysql = ColumnInfoMySQL(
                    id=f'{table.name}.{column_info.name}',
                    name=column_info.name,
                    type=column_types[column_info.name],
                    role=column_info.role,
                    description=column_info.description,
                    examples=column_values,
                    alias=column_info.alias,
                    table_id=table.name
                )
                column_infos.append(column_info_mysql)

        # 调用持久层的方法保存到table_info表中
        self.meta_mysql_repo.save_table_infos(table_infos)

        # 返回字段信息对象列表
        return column_infos

    async def _save_column_info_to_meta(self, column_infos: list[ColumnInfoMySQL]):
        # 调用持久层的方法保存到column_info表中
        self.meta_mysql_repo.save_column_infos(column_infos)


    async def _save_column_info_to_qdrant(self, column_infos: list[ColumnInfoMySQL]):
        # 遍历column_infos，对每一个column_info中的 name description 和 alias的每一个值进行向量化
        # point 包含（id,vector,payload）
        # id -> uuid生成
        # vector -> embedding模型向量化
        # payload -> 包含column_info中的所有信息的字典(ColumnInfoQdrant类型)

        # 收集所有点point的信息的字典列表
        # [{id:uuid,vector:'向量文本',payload:{}},{...}]
        pass


    async def _save_column_value_to_es(self, column_infos: list[ColumnInfoMySQL], tables: list[TableConfig]):
        pass

    async def _save_metric_info_to_meta(self, metrics: list[MetricConfig]) -> list[MetricInfoMySQL]:
        pass

    async def _save_column_metric_to_meta(self, metrics: list[MetricConfig]):
        pass

    async def _save_metric_info_to_qdrant(self, metric_infos: list[MetricInfoMySQL]):
        pass