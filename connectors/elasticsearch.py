from elasticsearch import Elasticsearch
from dotenv import dotenv_values
from pydantic import BaseModel
from pydantic import ValidationError
from typing import List

config = dotenv_values(".env")

class Log(BaseModel):
    topic_name: str
    payload : object

def create_index(index):
    client = Elasticsearch(config["ELASTICSEARCH_HOSTS"])
    result = client.indices.create(index=index)
    print(result)


def list_indices(index):
    return {}