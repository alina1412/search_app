from elasticsearch.exceptions import NotFoundError

from service.config import app


async def doc_delete(index_name, id):
    """by inner id"""
    app.state.elastic_client.delete(index=index_name, id=id)


async def doc_delete_from_index(index_name, id):
    """id - manual from schema"""
    query = {"query": {"term": {"id": id}}}
    res = app.state.elastic_client.search(index=index_name, body=query)
    # id = res.get("hits", {}).get("hits", [{}])[0].get("_source", {}).get("id")
    hits = res.get("hits", {}).get("hits", [{}])
    if not hits:
        raise NotFoundError
    inner_id = hits[0].get("_id")
    if not inner_id:
        raise NotFoundError
    app.state.elastic_client.delete(index=index_name, id=inner_id)
