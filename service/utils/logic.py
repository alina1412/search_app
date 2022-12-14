from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from service.db.crud import db_delete
from service.db.models import Documents


async def delete_doc_from_db(id: int, session: AsyncSession) -> None:
    await db_delete(session, Documents, (Documents.id == id,))
    await session.commit()


async def select_from_db_by_id(id_: int, session: AsyncSession) -> list:
    query = select(Documents).where(Documents.id == id_)
    results = (await session.execute(query)).all()
    return list(results)
