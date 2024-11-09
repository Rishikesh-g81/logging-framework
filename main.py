import connectors.kafka
from fastapi import FastAPI, HTTPException, Depends
import os
import importlib
import connectors
from connectors import kafka
from typing import List

app=FastAPI()

#KAFKA Endpoints
@app.get("/kafka/topics")
def get_kafka_topics():
    return connectors.kafka.list_topics()

@app.post("/kafka/topics" , status_code=201)
def create_kafka_topics(topics: List[connectors.kafka.Topic]):
    return connectors.kafka.create_topics(topics)

@app.post("/kafka/topic" , status_code=201)
def create_kafka_topics(topic : connectors.kafka.Topic):
    return connectors.kafka.create_topic(topic)

@app.post("/kafka/event", status_code=201)
def post_kafka_event(event: connectors.kafka.Event):
    return connectors.kafka.produce_event(event)

@app.post("/kafka/events", status_code=201)
def post_kafka_event(events: List[connectors.kafka.Event]):
    return connectors.kafka.produce_events(events)

#Elastic Search Endpoints