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

    async def get_db_info(self)->dict:
        # 获取数据库版本号
        result = await self.session.execute(text('select version()'))
        version = result.scalar()

        # 获取数据库名称（方言）
        dialect = self.session.get_bind().dialect.name

        return {"dialect": dialect, "version": version}

    async def validate_sql(self, sql: str):
        await self.session.execute(text(f'explain {sql}'))
        # 如果抛出异常，说明SQL不合法

    # 执行SQL
    async def to_execute_sql(self, sql: str)->list[dict]:
        result = await self.session.execute(text(sql))
        return [dict(row) for row in result.mappings().all()]
