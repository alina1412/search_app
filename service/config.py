from os import environ

from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from fastapi import FastAPI

load_dotenv()


class ElasticConfig:
    elastic_user = environ.get("ELASTIC_USER")
    elastic_password = environ.get("ELASTIC_PASSWORD")
    elastic_index = environ.get("ELASTIC_INDEX")
    elastic_host = environ.get("ELASTIC_HOST")
    elastic_host_port = environ.get("ELASTIC_H_PORT")
    elastic_size = 20
    assert elastic_user


class DBConfig:
    DATABASE_NAME: str = environ.get("DATABASE_NAME")
    POSTGRES_HOST: str = environ.get("POSTGRES_HOST", default="localhost")
    DATABASE_USERNAME: str = environ.get("DATABASE_USERNAME")
    POSTGRES_PORT: int = environ.get("POSTGRES_PORT")
    DATABASE_PASSWORD: str = environ.get("DATABASE_PASSWORD")


econf = ElasticConfig()
elastic_client = Elasticsearch(
    [f'http://{econf.elastic_host}:{econf.elastic_host_port}'], 
    basic_auth=(econf.elastic_user, econf.elastic_password),
)

# print(elastic_client.info())


app = FastAPI()
app.state.elastic_client = elastic_client
