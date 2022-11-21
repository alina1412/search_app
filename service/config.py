from os import environ

from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from fastapi import FastAPI

load_dotenv()


elastic_password = environ.get("ELASTIC_PASSWORD")
assert elastic_password

elastic_index = environ.get("ELASTIC_INDEX")
elastic_url= environ.get("ELASTIC_URL")
elastic_host_port= environ.get("ELASTIC_H_PORT")

class DBConfig:
    DATABASE_NAME: str = environ.get("DATABASE_NAME")
    POSTGRES_HOST: str = environ.get("POSTGRES_HOST", default="localhost")
    DATABASE_USERNAME: str = environ.get("DATABASE_USERNAME")
    POSTGRES_PORT: int = environ.get("POSTGRES_PORT")
    DATABASE_PASSWORD: str = environ.get("DATABASE_PASSWORD")


elastic_client = Elasticsearch(
    elastic_url + ":" + elastic_host_port,
    basic_auth=("elastic", elastic_password),
)

# print(elastic_client.info())


app = FastAPI()
app.state.elastic_client = elastic_client
