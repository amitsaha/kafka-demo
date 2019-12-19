import psutil
from kafka import KafkaProducer

import os
import time
import signal
import json
import logging


def publish_metrics(producer):
    cpu_usage_percent = psutil.cpu_percent()
    memory_usage_perecent = psutil.virtual_memory().percent
    data = {
        "node_id": "node123",
        "cpu_usage_percent": cpu_usage_percent,
        "memory_usage_percent": memory_usage_perecent,
        "timestamp": time.time(),
    }
    logging.info("Publishing metrics..")
    topic = os.getenv("KAFKA_TOPIC", "metrics")
    producer.send(topic, data)


def main():
    server = os.getenv("KAFKA_SERVER", "localhost:9092")
    producer = KafkaProducer(
        bootstrap_servers=server,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    logging.info("Obtained connection to Kafka broker")

    def handle_signals(signum, frame):
        print("Received signal: ", signum)
        producer.flush()
        producer.close()

    signal.signal(signal.SIGINT, handle_signals)

    while True:
        publish_metrics(producer)
        # Worth making this configurable
        time.sleep(10)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
