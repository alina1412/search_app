from elasticsearch.exceptions import NotFoundError
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from service.db.db_settings import get_session
from service.elastic.doc_delete import doc_delete_from_index
from service.elastic.errors import NotInElastic
from service.utils.logic import delete_doc_from_db

api_router = APIRouter(
    prefix="/v1",
    tags=["delete"],
)


@api_router.delete(
    "/delete-data",
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_404_NOT_FOUND: {"description": "Nothing to delete"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Bad request"},
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "description": "some error during deletion"
        },
    },
)
async def delete_one_handler(
    doc_id: int, index_name: str = "map", session: AsyncSession = Depends(get_session)
):
    """Deletes a document from bd and elastic index by id"""
    await delete_doc_from_db(doc_id, session)
    try:
        await doc_delete_from_index(index_name, doc_id)
    except NotInElastic:
        raise HTTPException(404, detail="nothing to delete")
    except Exception as exc:
        print(exc)
        return HTTPException(503, detail="some error during deletion")
