from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError
from starlette.requests import Request


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


async def get_all_by_index(request: Request, index: str):
    """get docs from elastic by index"""
    try:
        elastic_client: AsyncElasticsearch = request.app.state.elastic_client
        res = elastic_client.search(index=index, query={"match_all": {}})
        return {"success": True, "result": await prepare_results(res)}
    except NotFoundError:
        return "No such index to search"


searching = {
    "size": 2,
    "query": {"match": {"message": {"operator": "or", "query": "brown fox"}}},
    "rescore": {
        "window_size": 2,
        "query": {
            "rescore_query": {
                "match_phrase": {"message": {"query": "brown fox", "slop": 2}}
            },
            "query_weight": 0.7,
            "rescore_query_weight": 1.2,
        },
    },
}


async def get_matching_by_message(params: dict, request: Request):
    """search docs by field 'message' in mapping of elastic"""
    index_name = params["index_name"]
    searching["size"] = params["size"]
    searching["rescore"]["window_size"] = params["size"]
    searching["query"]["match"]["message"]["query"] = params["query"]
    # fmt: off
    searching["rescore"]["query"]["rescore_query"]["match_phrase"]["message"]["query"] = params["query"]
    # fmt: on

    try:
        elastic_client: AsyncElasticsearch = request.app.state.elastic_client
        res = elastic_client.search(index=index_name, body=searching)
        return {
            "result": await prepare_results(res),
            "ids": await prepare_id_of_results(res),
        }
    except NotFoundError:
        return "No such index to search"
        # 'index_not_found_exception'
