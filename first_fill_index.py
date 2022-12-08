import asyncio
from elasticsearch import AsyncElasticsearch
from sqlalchemy.ext.asyncio import create_async_engine

from service.config import app, econf
from service.db.crud import db_select
from service.db.db_settings import async_database_uri
from service.db.models import Documents
from service.elastic.mapping import mapping_for_index, elastic_text_settings
from service.schemas import TextInput


async def create_index_for_docs():
    try:
        elastic_client: AsyncElasticsearch = app.state.elastic_client
        elastic_client.indices.create(
            index=econf.elastic_index,
            mappings=mapping_for_index,
            settings=elastic_text_settings,
        )
    except Exception:
        pass


async def if_doc_with_id_exists(id_):
    result = app.state.elastic_client.search(
        index=econf.elastic_index, query={"term": {"id": id_}}
    )
    items = result.get("hits", {}).get("hits", [{}])
    if len(items) > 0:
        print("--alreay in index: ", items[0]["_source"])
        print()
        return True
    return False


async def elastic_insert(insert_data: TextInput):
    if not await if_doc_with_id_exists(insert_data.id):
        app.state.elastic_client.index(index=econf.elastic_index, document=insert_data.dict())


async def fill_from_db():
    await create_index_for_docs()

    engine = create_async_engine(async_database_uri(), echo=True, future=True)
    async with engine.connect() as session:

        data = await db_select(
            session,
            (
                Documents.id,
                Documents.text,
            ),
            (True,),
        )
        for id_, message in data:
            item = TextInput(id=id_, message=message)
            await elastic_insert(item)
            


if __name__ == "__main__":
    asyncio.run(fill_from_db())
    