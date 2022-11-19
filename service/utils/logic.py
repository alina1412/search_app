from sqlalchemy.ext.asyncio import create_async_engine

from service.db.crud import db_delete
from service.db.db_settings import async_database_uri
from service.db.models import Documents


async def delete_doc_from_db(id: int):
    engine = create_async_engine(async_database_uri(), echo=True, future=True)
    async with engine.connect() as session:
        from sqlalchemy import delete
        # query = delete(Documents).where(Documents.id = id)
        query = f"DELETE FROM documents WHERE documents.id = {id}"
        await session.execute(query)
        # await db_delete(session, Documents, {"documents.id": id})
        await session.commit()
