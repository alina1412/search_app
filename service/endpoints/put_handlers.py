from elasticsearch import AsyncElasticsearch, RequestError
from fastapi import APIRouter, Depends, status
from starlette.requests import Request

from service.elastic.bulk_insert import bulk_insert
from service.schemas import UserInput


api_router = APIRouter(
    prefix="/v1",
    tags=["data"],
)


@api_router.put(
    "/add-data",
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Bad request"},
    },
)
async def create_data_handler(request: Request, user: UserInput):
    """"""
    elastic_client: AsyncElasticsearch = request.app.state.elastic_client
    res = elastic_client.index(index="users", document=user.dict())
    print(res)
    return {"success": True, "result": res}


insert_data = [
    {
        "id": 1,
        "name": "EEE",
        "surname": "BBB",
        "date_of_birth": "2022-11-18",
        "interests": ["III"],
    },
    {
        "id": 2,
        "name": "CCC",
        "surname": "DDD",
        "date_of_birth": "2022-11-18",
    },
]


@api_router.put(
    "/add-bulk-data",
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Bad request"},
    },
)
async def create_many_handler(
    request: Request,
):
    """"""
    try:
        await bulk_insert(insert_data)
    except Exception as exc:
        ...
    return {"success": True}
