from typing import Type

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from service.db.models import DeclarativeBase


async def db_insert(
    session: AsyncSession, model: Type[DeclarativeBase], dict_data
) -> None:
    query = insert(model).values(**dict_data)
    await session.execute(query)


async def db_select(session: AsyncSession, what: tuple, condition: tuple) -> list:
    query = select(*what).where(*condition)
    results = (await session.execute(query)).all()
    return list(results)


async def db_update(
    session: AsyncSession, what: Type[DeclarativeBase], condition: tuple, new_data
) -> None:
    try:
        stmt = update(*what).where(*condition).values(**new_data)
        await session.execute(stmt)
    except Exception as exc:
        print(exc)
        await session.rollback()


async def db_delete(
    session: AsyncSession, what: Type[DeclarativeBase], condition: tuple
) -> None:
    query = delete(what).where(*condition)
    await session.execute(query)
