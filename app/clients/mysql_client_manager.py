import asyncio

from sqlalchemy import text, Select
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession, async_sessionmaker

from app.conf.app_config import DBConfig, app_config
from app.models.mysql.table_info_mysql import TableInfoMySQL


# 操作mysql数据库的客户端管理器
class MysqlClientManager:
    # 初始化实例属性
    def __init__(self, config: DBConfig):
        self.config = config
        self.engine: AsyncEngine | None = None
        self.session_factory: async_sessionmaker | None = None

    # 获取连接的url
    def _get_url(self):
        return f"mysql+asyncmy://{self.config.user}:{self.config.password}@{self.config.host}:{self.config.port}/{self.config.database}?charset=utf8mb4"

    # 初始化客户端
    def init(self):
        # 创建异步引擎
        self.engine = create_async_engine(
            self._get_url(),
            pool_size=10,  # 初始创建的常驻连接池的连接数量
            pool_pre_ping=True  # 每次连接使用前进行一次ping操作，确认连接是否可用
        )

        # 创建异步会话的工厂
        self.session_factory = async_sessionmaker(
            self.engine,
            autoflush=True,  # 自动刷新数据，自动将未提交事务的修改数据同步到数据库暂存区，可以查询到最新的数据
            autobegin=True,  # 自动开始事务，每次执行sql语句前自动开始事务，并不会自动关闭事务
            expire_on_commit=False  # 提交事务后ORM对象不过期，还可以访问里面的数据
        )

    # 关闭客户端
    async def close(self):
        await self.engine.dispose()


# 创建操作数据库的客户端
dw_mysql_client_manager = MysqlClientManager(config=app_config.db_dw)
meta_mysql_client_manager = MysqlClientManager(config=app_config.db_meta)

# 测试
if __name__ == '__main__':
    async def test1():
        # 初始化客户端
        dw_mysql_client_manager.init()

        # 创建异步会话
        session = AsyncSession(dw_mysql_client_manager.engine)
        # 使用会话操作数据库
        # text("select * from dim_customer limit 2") 将sql字符串转成可执行对象
        result = await session.execute(text("select * from dim_customer limit 2"))
        # print(result) # <sqlalchemy.engine.cursor.CursorResult object at 0x000002011CD2ECF0>

        # 获取查询结果
        # rows = result.all() # 得到row列表
        # print(rows) # [('C001', '李伟', '男', '黄金'), ('C002', '王芳', '女', '白银')]

        # rows = result.mappings().all() # 得到mapping字典列表
        # print(rows) # [{...},{...}]

        # rows = result.scalars().all() # 得到每一行的第一列数据
        # print(rows) # ['C001', 'C002']

        rows = result.scalar()  # 得到第一个值
        print(rows)  # C001

        # 关闭会话
        await session.close()

        # 关闭客户端，释放资源
        await dw_mysql_client_manager.close()


    # asyncio.run(test1())

    async def test2():
        # 初始化客户端
        dw_mysql_client_manager.init()

        async with dw_mysql_client_manager.session_factory() as session:
            result = await session.execute(text("select * from dim_customer limit 2"))

            # 获取查询结果
            # rows = result.all() # 得到row列表
            # print(rows) # [('C001', '李伟', '男', '黄金'), ('C002', '王芳', '女', '白银')]

            # rows = result.mappings().all() # 得到mapping字典列表
            # print(rows) # [{...},{...}]

            # rows = result.scalars().all() # 得到每一行的第一列数据
            # print(rows) # ['C001', 'C002']

            rows = result.scalar()  # 得到第一个值
            print(rows)  # C001

        # 关闭客户端，释放资源
        await dw_mysql_client_manager.close()


    # asyncio.run(test2())

    async def test3():
        # 使用ORM操作数据库

        # 初始化客户端
        meta_mysql_client_manager.init()

        async with meta_mysql_client_manager.session_factory() as session:
            # 创建ORM对象
            table_info1 = TableInfoMySQL(
                id='11',
                name='test_table1',
                role='fact',
                description='测试表1'
            )
            table_info2 = TableInfoMySQL(
                id='22',
                name='test_table2',
                role='fact',
                description='测试表2'
            )

            # 添加数据
            # session.add(table_info1)
            # session.add(table_info2)

            # 提交事务
            # await session.commit()

            # 提交后访问ORM对象里的数据
            # print(table_info1.name) # test_table1

            # 查询一条数据
            # result = await session.get(TableInfoMySQL,'11')
            # print(result)
            # print(result.name) # test_table1

            # 查询多条数据
            # result = await session.execute(Select(TableInfoMySQL).limit(2))
            # print(result)
            # rows: list[TableInfoMySQL] = result.scalars().all()
            # print(rows) # [TableInfoMySQL Object,TableInfoMySQL Object]
            # print(rows[0].name) # test_table1

            # result = await session.execute(text("select * from dim_customer limit 2"))

            # 删除数据
            # table_info3 = await session.get(TableInfoMySQL,'dim_date')
            # await session.delete(table_info3)

            # 修改数据
            table_info4 = await session.get(TableInfoMySQL, '22')
            table_info4.name = 'test_table123'

            # 提交事务
            await session.commit()

        # 关闭客户端，释放资源
        await meta_mysql_client_manager.close()


    asyncio.run(test3())
