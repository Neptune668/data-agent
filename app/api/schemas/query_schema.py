from pydantic import BaseModel

# 定义body参数的数据结构
class QuerySchema(BaseModel):
    query: str
