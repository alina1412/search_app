from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from service.config import DBConfig


def connect_string() -> str:
    """string without a driver"""
    return (
        f"{DBConfig.DATABASE_USERNAME}:{DBConfig.DATABASE_PASSWORD}"
        f"@{DBConfig.POSTGRES_HOST}:{DBConfig.POSTGRES_PORT}/{DBConfig.DATABASE_NAME}"
    )


def async_database_uri() -> str:
    """Return the async database URL."""
    return "postgresql+asyncpg://" + connect_string()


def sync_database_uri() -> str:
    """Return the sync database URL."""
    return "postgresql://" + connect_string()


class DBManager:
    @property
    def uri(self):
        return async_database_uri()

    @property
    def engine(self):
        return create_async_engine(self.uri, echo=True, future=True)

    @property
    def session_maker(self):
        return sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator:
    async with DBManager().session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception as exc:
            await session.rollback()
            raise exc
        finally:
            await session.close()
