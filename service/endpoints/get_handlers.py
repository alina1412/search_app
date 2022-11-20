from elasticsearch import AsyncElasticsearch, RequestError
from fastapi import APIRouter, Depends, Query, status
from fastapi.exceptions import HTTPException
from starlette.requests import Request

from service.db.db_settings import get_session
from service.elastic.search import get_all_users, get_matching_by_message
from service.utils.logic import select_from_id_list

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
async def get_all_users_handler(request: Request):
    """"""
    return await get_all_users(request)


@api_router.get(
    "/match-data",
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Bad request"},
    },
)
async def get_matching_handler(
    request: Request,
    session=Depends(get_session),
    query: str = Query(default=None, min_length=2),
):
    """"""
    if not query.strip():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="nothing to search")
    return await get_matching_by_message(query, request)


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
    await select_from_id_list(session, id_list)
    return
