from fastapi import APIRouter, status
from starlette.requests import Request

from service.elastic.doc_delete import doc_delete_from_index
from service.utils.logic import delete_doc_from_db


api_router = APIRouter(
    prefix="/v1",
    tags=["delete"],
)


@api_router.delete(
    "/delete-data",
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Bad request"},
    },
)
async def delete_one_handler(
    request: Request,
    id,
    index_name: str = "users",
):
    """"""
    response = await doc_delete_from_index(index_name, id)
    await delete_doc_from_db(id)
    return response
