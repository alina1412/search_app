from fastapi import APIRouter, Depends, status
from starlette.requests import Request
from service.config import app

from elasticsearch import AsyncElasticsearch, RequestError
from service.db.fake_db import MAPPING_FOR_INDEX

api_router = APIRouter(
    prefix="/v1",
    tags=["private"],
)


@api_router.post(
    "/create-index",
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Bad request"},
        
    },
)
async def create_index(
    request: Request,
    # user_input: User = Depends(),
    # user_token_data=Depends(get_user_by_token)
):
    """"""
    elastic_client: AsyncElasticsearch = request.app.state.elastic_client
    app.state.elastic_client.indices.create(index="users", mappings=MAPPING_FOR_INDEX)
    return {"success": True}
