from elasticsearch import AsyncElasticsearch, RequestError
from elasticsearch.exceptions import BadRequestError, NotFoundError
from fastapi import APIRouter, Depends, status
from starlette.requests import Request

from service.config import app
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
    try:
        elastic_client: AsyncElasticsearch = request.app.state.elastic_client
        elastic_client.indices.create(index="users", mappings=MAPPING_FOR_INDEX)
    except BadRequestError as exc:
        if exc.error == 'resource_already_exists_exception':
            return {'resource_already_exists_exception'}
        else:
            print("sometihg else")
            assert exc == ""
    return {"success": True}


@api_router.post(
    "/delete-index",
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Bad request"},
        
    },
)
async def delete_index(
    request: Request,
    # user_input: User = Depends(),
    # user_token_data=Depends(get_user_by_token)
):
    """"""
    try:
        elastic_client: AsyncElasticsearch = request.app.state.elastic_client
        elastic_client.indices.delete(index="users")
    
        return {"success": True}
    except NotFoundError:
        return ("No index to delete")