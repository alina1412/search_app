from elasticsearch import AsyncElasticsearch, RequestError
from fastapi import APIRouter, Depends, status
from starlette.requests import Request

from service.elastic.search import get_all_users, get_matching_by_message


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
async def get_matching_handler(query: str, request: Request):
    """"""
    return await get_matching_by_message(query, request)
