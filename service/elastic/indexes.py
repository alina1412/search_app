from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import BadRequestError, NotFoundError
from starlette.requests import Request

from service.elastic.mapping import mapping_for_index, elastic_text_settings


async def create_index(request: Request, index_name: str):
    """"""
    try:
        elastic_client: AsyncElasticsearch = request.app.state.elastic_client
        elastic_client.indices.create(
            index=index_name, mappings=mapping_for_index, settings=elastic_text_settings
        )
    except BadRequestError as exc:
        if exc.error == "resource_already_exists_exception":
            return {"resource_already_exists_exception"}
        raise exc
    return {"success": True}


async def delete_index(request: Request, index_name: str):
    """"""
    try:
        elastic_client: AsyncElasticsearch = request.app.state.elastic_client
        elastic_client.indices.delete(index=index_name)
        return {"success": True}
    except NotFoundError:
        return "No index to delete"
