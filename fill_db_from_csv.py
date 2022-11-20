import asyncio
import csv
from datetime import datetime


from sqlalchemy.ext.asyncio import create_async_engine
from service.db.db_settings import async_database_uri
from service.db.crud import db_insert
from service.db.models import Documents


def get_tuple_from_csv():
    """['text,created_date,rubrics']"""
    with open("posts.csv", "r", newline="") as csvfile:
        docreader = csv.reader(csvfile)
        next(docreader)
        for row in docreader:
            yield row


async def fill_db():
    engine = create_async_engine(async_database_uri(), echo=True, future=True)
    async with engine.connect() as session:
        for text, created_date, rubrics in get_tuple_from_csv():
            created_date = created_date.replace(" ", "T")
            data = datetime.strptime(created_date, "%Y-%m-%dT%H:%M:%S")

            await db_insert(
                session,
                Documents,
                {"rubrics": rubrics, "text": text, "created_date": data},
            )
            await session.commit()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        asyncio.run(fill_db())
    except KeyboardInterrupt:
        pass
