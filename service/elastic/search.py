from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from service.elastic.errors import NoIndex
from service.utils.logic import select_from_db_by_id


async def prepare_results(results) -> list[dict]:
    # id = res.get("hits", {}).get("hits", [{}])[0].get("_source", {}).get("id")
    source_res = []
    for elem in results.get("hits", {}).get("hits", [{}]):
        source_res.append(elem["_source"])
    return source_res


async def prepare_inner_id_of_results(results) -> list[str]:
    """ids which created automatically by elastic"""
    id_res = []
    for elem in results.get("hits", {}).get("hits", [{}]):
        id_res.append(elem["_id"])
    return id_res


async def prepare_id_of_results(results) -> list[int]:
    """the field id given by schema"""
    id_res = []
    for elem in results.get("hits", {}).get("hits", [{}]):
        id = elem.get("_source", {}).get("id")
        id_res.append(id)
    return id_res


async def prepare_searching_query(params) -> dict:
    searching = {
        "size": params["size"],
        "query": {"match": {"message": {"operator": "or", "query": params["query"]}}},
        "rescore": {
            "window_size": params["size"],
            "query": {
                "rescore_query": {
                    "match_phrase": {"message": {"query": params["query"], "slop": 2}}
                },
                "query_weight": 0.7,
                "rescore_query_weight": 1.2,
            },
        },
    }
    return searching


async def get_matching_dict(index_name, searching, request) -> dict:
    try:
        elastic_client: AsyncElasticsearch = request.app.state.elastic_client
        res = elastic_client.search(index=index_name, body=searching)
        return dict(res)
    except NotFoundError:
        raise NoIndex


async def get_matching_by_message(
    params: dict, request: Request, session: AsyncSession
) -> dict:
    """search docs by field 'message' in mapping of elastic"""
    searching = await prepare_searching_query(params)
    index_name = params["index_name"]
    res_from_elastic = await get_matching_dict(index_name, searching, request)
    ids = await prepare_id_of_results(res_from_elastic)
    data = []
    for id_ in ids:
        data.extend(await select_from_db_by_id(id_, session))
    return {"data": data}
