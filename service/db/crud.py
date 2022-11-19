from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


async def db_insert(session: AsyncSession, model, dict_data) -> None:
    query = insert(model).values(**dict_data)
    await session.execute(query)


async def db_select(session: AsyncSession, what, condition) -> list:
    query = select(*what).where(*condition)
    results = (await session.execute(query)).all()
    return list(results)


async def db_update(session: AsyncSession, what, condition, new_data) -> None:
    try:
        stmt = update(*what).where(*condition).values(**new_data)
        await session.execute(stmt)
    except Exception as exc:
        print(exc)
        await session.rollback()


async def db_delete(session: AsyncSession, what, condition) -> None:
    query = delete(*what).where(*condition)
    await session.execute(query)
