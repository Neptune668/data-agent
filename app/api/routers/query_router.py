from fastapi import APIRouter, Depends

from app.api.dependencies import get_query_service
from app.api.schemas.query_schema import QuerySchema
from app.services.query_service import QueryService
from fastapi.responses import StreamingResponse

# 创建路由器
query_router = APIRouter()

# 注册路由（接口）
@query_router.post('/api/query')
async def query(query_schema: QuerySchema, q_service: QueryService = Depends(get_query_service)):
    # 流式响应
    return StreamingResponse(
        q_service.search(query_schema.query),
        media_type="text/event-stream"
    )
