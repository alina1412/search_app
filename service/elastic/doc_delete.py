from service.config import app
from service.elastic.errors import NotInElastic


async def doc_delete_from_index(
    index_name: str,
    id: int,
) -> None:
    """deletes doc from index in elastic by id
    id - manual from schema (should be unique)"""
    query = {"query": {"term": {"id": id}}}
    res = app.state.elastic_client.search(index=index_name, body=query)
    # id = res.get("hits", {}).get("hits", [{}])[0].get("_source", {}).get("id")
    hits = res.get("hits", {}).get("hits", [{}])
    if not hits:
        raise NotInElastic
    inner_id = hits[0].get("_id")
    if not inner_id:
        raise NotInElastic
    app.state.elastic_client.delete(index=index_name, id=inner_id)
