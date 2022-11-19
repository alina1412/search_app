from elasticsearch import AsyncElasticsearch, RequestError
from fastapi import APIRouter, Depends, status
from starlette.requests import Request

from service.schemas import UserInput

api_router = APIRouter(
    prefix="/v1",
    tags=["search"],
)


@api_router.post(
    "/all-data",
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Bad request"},
    },
)
async def get_all_users(request: Request):
    """"""
    elastic_client: AsyncElasticsearch = request.app.state.elastic_client
    res = elastic_client.search(index="users", query={"match_all": {}})
    return {"success": True, "result": res}
