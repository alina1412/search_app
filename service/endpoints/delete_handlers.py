from elasticsearch.exceptions import NotFoundError
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
    doc_id: int,
    index_name: str = "map",
):
    """"""
    try:
        await doc_delete_from_index(index_name, doc_id)
    except NotFoundError:
        return {"nothing to delete"}
    except Exception as exc:
        print(exc)
        return {"some error during deletion"}
    await delete_doc_from_db(doc_id)
    # return response
