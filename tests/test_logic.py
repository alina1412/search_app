import datetime
import uuid

from service.db.crud import db_insert, db_select
from service.db.models import Documents
from service.utils.logic import delete_doc_from_db


async def test_db_insert(db):
    """makes inertion, checks if it's there"""
    data = datetime.datetime.strptime("2022-05-24T15:55:05", "%Y-%m-%dT%H:%M:%S")
    text = str(uuid.uuid4())

    row = await db_select(db, (Documents.text,), (Documents.text == text,))
    assert not list(row)

    await db_insert(
        db, Documents, {"text": text, "rubrics": "[a]", "created_date": data}
    )
    await db.commit()

    row = await db_select(db, (Documents.text,), (Documents.text == text,))
    assert row[0][0] == text


async def test_deletion(db):
    """runs after something was inserted"""
    row = await db_select(db, (Documents.id,), (True,))
    id_ = row[0][0]
    await delete_doc_from_db(id_, db)

    row = await db_select(db, (Documents.id,), (Documents.id == id_,))
    assert not list(row)
