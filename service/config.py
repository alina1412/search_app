from os import environ

from dotenv import load_dotenv
from fastapi import FastAPI
from elasticsearch import AsyncElasticsearch, Elasticsearch, RequestError


load_dotenv()


ELASTIC_PASSWORD = environ.get("ELASTIC_PASSWORD")
assert ELASTIC_PASSWORD


elastic_client = Elasticsearch(
    "http://localhost:9200",
    basic_auth=("elastic", ELASTIC_PASSWORD),
)

print(elastic_client.info())


app = FastAPI()
app.state.elastic_client = elastic_client
