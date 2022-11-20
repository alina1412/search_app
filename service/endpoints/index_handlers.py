from fastapi import APIRouter, status
from starlette.requests import Request

from service.elastic.indexes import create_index, delete_index

api_router = APIRouter(
    prefix="/v1",
    tags=["indexes"],
)


@api_router.put(
    "/create-index",
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Bad request"},
    },
)
async def create_index_handler(request: Request, index_name: str = "users"):
    """"""
    return await create_index(request, index_name)


@api_router.delete(
    "/delete-index",
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Bad request"},
    },
)
async def delete_index_handler(request: Request, index_name: str = "users"):
    """"""
    return await delete_index(request, index_name)
