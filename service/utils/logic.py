from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine

from service.db.crud import db_delete, db_select
from service.db.db_settings import async_database_uri, get_session
from service.db.models import Documents


async def delete_doc_from_db(id: int):
    engine = create_async_engine(async_database_uri(), echo=True, future=True)
    async with engine.connect() as session:
        await db_delete(session, Documents, (Documents.id == id,))
        await session.commit()


async def select_from_db_by_ids(lst, session):
    query = select(Documents).where(Documents.id.in_(lst)).order_by(Documents.created_date).limit(20)
    results = (await session.execute(query)).all()
    return list(results)

    # cursor = await db_select(
    #     session, (Documents.id, Documents.text), (Documents.id.in_(lst),)
    # )
    # print(list(cursor))
