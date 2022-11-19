from elasticsearch.exceptions import NotFoundError

from service.config import app


async def doc_delete(index_name, id):
    """by inner id"""
    app.state.elastic_client.delete(index=index_name, id=id)


async def doc_delete_from_index(index_name, id):
    query = {"query": {"term": {"id": id}}}

    try:
        res = app.state.elastic_client.search(index=index_name, body=query)
        # id = res.get("hits", {}).get("hits", [{}])[0].get("_source", {}).get("id")
        hits = res.get("hits", {}).get("hits", [{}])
        if hits:
            inner_id = hits[0].get("_id")
        elif not hits:
            return {"nothing to delete"}
        if not inner_id:
            return {"nothing to delete"}

        app.state.elastic_client.delete(index=index_name, id=inner_id)
    except NotFoundError:
        return {"nothing to delete"}
    return {"ok"}
