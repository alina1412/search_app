from os import environ
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()
key = environ.get("key")

from elasticsearch import AsyncElasticsearch, RequestError
from elasticsearch import Elasticsearch


ELASTIC_PASSWORD = environ.get("ELASTIC_PASSWORD")
assert ELASTIC_PASSWORD


elastic_client = Elasticsearch(
    "http://localhost:9200",
    basic_auth=("elastic", ELASTIC_PASSWORD),
)

print(elastic_client.info())


app = FastAPI()
app.state.elastic_client = elastic_client
