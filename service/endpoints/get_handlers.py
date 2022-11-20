from fastapi import APIRouter, Depends, Query, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from service.config import elastic_index
from service.db.db_settings import get_session
from service.elastic.errors import NoIndex
from service.elastic.search import get_matching_by_message

api_router = APIRouter(
    prefix="/v1",
    tags=["search"],
)


@api_router.get(
    "/match-data",
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Bad request"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {},
    },
)
async def get_matching_handler(
    request: Request,
    query: str = Query(default="", min_length=2),
    session: AsyncSession = Depends(get_session),
):
    """gets matching docs from elastic by query,
    return first N(20) docs from all bd fields, order by data"""
    if not query.strip():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="nothing to search")

    params = {"query": query, "size": 20, "index_name": elastic_index}
    try:
        res = await get_matching_by_message(params, request, session)
        return res
    except NoIndex:
        return HTTPException(500, f"No such index '{elastic_index}' to search")
