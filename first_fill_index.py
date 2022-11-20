import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

from service.db.db_settings import async_database_uri
from service.db.crud import db_select
from service.db.models import Documents
from service.schemas import TextInput
from service.config import elastic_index, app


async def elastic_insert(insert_data: TextInput):
    app.state.elastic_client.index(index=elastic_index, document=insert_data.dict())


async def fill_from_db():
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
