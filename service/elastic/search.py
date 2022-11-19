from elasticsearch import AsyncElasticsearch
from starlette.requests import Request
from elasticsearch.exceptions import NotFoundError


async def get_all_users(request: Request):
    """"""
    elastic_client: AsyncElasticsearch = request.app.state.elastic_client
    res = elastic_client.search(index="users", query={"match_all": {}})
    return {"success": True, "result": res}


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


async def get_matching(query: str, request: Request):
    """"""
    searching["query"]["match"]["message"]["query"] = query
    # fmt: off
    searching["rescore"]["query"]["rescore_query"]["match_phrase"]["message"]["query"] = query
    # fmt: on

    try:
        elastic_client: AsyncElasticsearch = request.app.state.elastic_client
        res = elastic_client.search(index="users", body=searching)
        return {"success": True, "result": res}
    except NotFoundError:
        return "No such index to search"
        # 'index_not_found_exception'
