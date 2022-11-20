from service.config import app
from service.schemas import UserInput
from service.config import elastic_index

async def bulk_insert(insert_data: list[UserInput]):
    for item in insert_data:
        app.state.elastic_client.index(index=elastic_index, document=item)
