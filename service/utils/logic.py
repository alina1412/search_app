from sqlalchemy.ext.asyncio import create_async_engine

from service.db.crud import db_delete, db_select
from service.db.db_settings import async_database_uri
from service.db.models import Documents


async def delete_doc_from_db(id: int):
    engine = create_async_engine(async_database_uri(), echo=True, future=True)
    async with engine.connect() as session:
        await db_delete(session, Documents, (Documents.id == id,))
        await session.commit()


async def select_from_id_list(session, lst):
    cursor = await db_select(
        session, (Documents.id, Documents.text), (Documents.id.in_(lst),)
    )
    print(list(cursor))
