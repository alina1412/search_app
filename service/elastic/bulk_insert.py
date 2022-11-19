from service.config import app
from service.schemas import UserInput


async def bulk_insert(insert_data: list[UserInput]):
    for item in insert_data:
        app.state.elastic_client.index(index="users", document=item)
