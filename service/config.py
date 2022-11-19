from os import environ

from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from fastapi import FastAPI

load_dotenv()


ELASTIC_PASSWORD = environ.get("ELASTIC_PASSWORD")
assert ELASTIC_PASSWORD


class DBConfig:
    DATABASE_NAME: str = environ.get("DATABASE_NAME")
    POSTGRES_HOST: str = environ.get("POSTGRES_HOST", default="localhost")
    DATABASE_USERNAME: str = environ.get("DATABASE_USERNAME")
    POSTGRES_PORT: int = environ.get("POSTGRES_PORT")
    DATABASE_PASSWORD: str = environ.get("DATABASE_PASSWORD")


elastic_client = Elasticsearch(
    "http://localhost:9200",
    basic_auth=("elastic", ELASTIC_PASSWORD),
)

# print(elastic_client.info())


app = FastAPI()
app.state.elastic_client = elastic_client
