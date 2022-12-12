import asyncio
import csv
from datetime import datetime

from sqlalchemy.ext.asyncio import create_async_engine

from service.db.db_settings import async_database_uri # isort: skip
from service.db.crud import db_insert # isort: skip
from service.db.models import Documents # isort: skip


def get_tuple_from_csv():
    """text, created_date, rubrics"""
    with open("posts.csv", "r", newline="", encoding="utf-8") as csvfile:
        docreader = csv.reader(csvfile)
        next(docreader)
        for row in docreader:
            yield row


async def fill_db():
    engine = create_async_engine(async_database_uri(), echo=True, future=True)
    async with engine.connect() as session:
        for text, created_date, rubrics in get_tuple_from_csv():
            created_date = created_date.replace(" ", "T")
            date = datetime.strptime(created_date, "%Y-%m-%dT%H:%M:%S")

            await db_insert(
                session,
                Documents,
                {"text": text, "rubrics": rubrics, "created_date": date},
            )
            await session.commit()


if __name__ == "__main__":
    asyncio.run(fill_db())
   