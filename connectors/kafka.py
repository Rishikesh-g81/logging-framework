from kafka import KafkaProducer, KafkaConsumer, KafkaAdminClient
from kafka.admin.new_topic import NewTopic
from kafka.errors import *
import json
from dotenv import dotenv_values
from pydantic import BaseModel
from pydantic import ValidationError
from typing import List

config = dotenv_values(".env")

class Event(BaseModel):
    topic_name: str
    payload : object

class Topic(BaseModel):
    topic_name: str
    num_partitions: int
    replication_factor: int


def produce_event(event : Event):
    producer=KafkaProducer(bootstrap_servers=config["KAFKA_BROKERS"])
    json_data = json.dumps(event.payload).encode("utf-8")
    
    topic=event.topic_name

    producer.send(topic, json_data)
    producer.flush()
    producer.close()
    return {
        "message" : f"Sent event data to topic: {topic}",
        "payload" : event
    }

def produce_events(events : List[Event]):
    producer=KafkaProducer(bootstrap_servers=config["KAFKA_BROKERS"])

    response=[]

    for event in events:

        json_data = json.dumps(event.payload).encode("utf-8")
        
        topic=event.topic_name

        producer.send(topic, json_data)
        producer.flush()
        producer.close()
        response.append({
            "message" : f"Sent event data to topic: {topic}",
            "payload" : event
        })

    return response

def list_topics():
    admin_client = KafkaAdminClient(
        bootstrap_servers=config["KAFKA_BROKERS"],
        client_id='kafka-python-' + config["KAFKA_PYTHON_VERSION"]
    )

    topics = admin_client.list_topics()
    return {
        "message" : "Topics returned successfully.",
        "payload" : topics
    }

def create_topic(topic : Topic):
    try:
        admin_client = KafkaAdminClient(
            bootstrap_servers=config["KAFKA_BROKERS"],
            client_id='kafka-python-' + config["KAFKA_PYTHON_VERSION"]
        )
        new_topic = NewTopic(name=topic.topic_name, num_partitions=topic.num_partitions, replication_factor=topic.replication_factor)
        admin_client.create_topics(new_topics=[new_topic],validate_only=False)
        return {
            "message" : "Topic {} created successfully.".format(topic.topic_name),
            "payload" : topic
        }
    except Exception as e:
        return {
        "message" : "Failed to create Topic {}.".format(topic.topic_name),
        "error" : e.__class__,
        "description" : str(e),
    }

def create_topics(topics : List[Topic]):
    try:
        admin_client = KafkaAdminClient(
            bootstrap_servers=config["KAFKA_BROKERS"],
            client_id='kafka-python-' + config["KAFKA_PYTHON_VERSION"]
        )
        new_topics = [NewTopic(name=topic.topic_name, num_partitions=topic.num_partitions, replication_factor=topic.replication_factor) for topic in topics]
        admin_client.create_topics(new_topics=new_topics,validate_only=False)
        return {
            "message" : "Topics created successfully.",
            "payload" : topics
        }
    except Exception as e:
        return {
        "message" : "Topics not created successfully.",
        "error" : e.__class__,
        "description" : str(e),
    }