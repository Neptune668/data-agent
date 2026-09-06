from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class DWMySQLRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # 获取字段的类型
    async def get_column_types(self, table_name: str)->dict:
        sql = f'show columns from {table_name}'
        result = await self.session.execute(text(sql))
        return {row.Field: row.Type for row in result.all()}

    # 获取字段的值
    async def get_column_values(self, table_name: str, column_name: str, limit: int = 10)->list:
        sql = f'select distinct {column_name} from {table_name} limit {limit}'
        result = await self.session.execute(text(sql))
        return result.scalars().all()

