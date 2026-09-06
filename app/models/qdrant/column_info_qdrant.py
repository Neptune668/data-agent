from typing import TypedDict

# 纯字典：访问属性不方便，每一提示，类型很宽泛  user1: dict[str,int] 字典所有的键都是str，值都是int

class ColumnInfoQdrant(TypedDict):
    id: str
    name: str
    role: str
    type: str
    description: str
    alias: list[str]
    examples: list[str]
    table_id: str