import asyncio
from elasticsearch import AsyncElasticsearch
from sqlalchemy.ext.asyncio import create_async_engine

from service.db.db_settings import async_database_uri
from service.db.crud import db_select
from service.db.models import Documents
from service.elastic.mapping import mapping_for_index, elastic_text_settings
from service.schemas import TextInput
from service.config import elastic_index, app


async def create_index_for_docs():
    try:
        elastic_client: AsyncElasticsearch = app.state.elastic_client
        elastic_client.indices.create(
            index=elastic_index,
            mappings=mapping_for_index,
            settings=elastic_text_settings,
        )
    except Exception:
        pass


async def elastic_insert(insert_data: TextInput):
    app.state.elastic_client.index(index=elastic_index, document=insert_data.dict())


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
        for id, message in data:
            item = TextInput(id=id, message=message)
            await elastic_insert(item)
            # break


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        asyncio.run(fill_from_db())
    except KeyboardInterrupt:
        pass
