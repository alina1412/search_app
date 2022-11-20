from elasticsearch import AsyncElasticsearch, RequestError
from fastapi import APIRouter, Depends, Query, status
from fastapi.exceptions import HTTPException
from starlette.requests import Request

from service.db.db_settings import get_session
from service.elastic.search import get_all_by_index, get_matching_by_message
from service.utils.logic import select_from_db_by_ids
from service.config import elastic_index


api_router = APIRouter(
    prefix="/v1",
    tags=["search"],
)


@api_router.get(
    "/all-data",
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Bad request"},
    },
)
async def get_all_docs_handler(request: Request, index: str):
    """gets all docs from elastic by index"""
    return await get_all_by_index(request, index)


@api_router.get(
    "/match-data",
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Bad request"},
    },
)
async def get_matching_handler(
    request: Request,
    query: str = Query(default="", min_length=2),
):
    """gets matching docs from elastic by query"""
    if not query.strip():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="nothing to search")

    params = {
        "query": query,
        "size": 20,
        "index_name": elastic_index
    }
    return await get_matching_by_message(params, request)


@api_router.get(
    "/ids",
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Bad request"},
    },
)
async def get_from_id_list_handler(
    request: Request, id_list: list[int] = Query(), session=Depends(get_session)
):
    """get from db by list of id"""
    results = await select_from_db_by_ids(id_list, session)
    return {"lst" : results}
