from sqlalchemy.ext.asyncio import AsyncSession

from app.models.mysql.table_info_mysql import TableInfoMySQL


class MetaMySQLRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # 向table_info表添加多条数据
    def save_table_infos(self, table_infos: list[TableInfoMySQL]):
        self.session.add_all(table_infos)

