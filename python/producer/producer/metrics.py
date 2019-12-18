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
            'cpu_usage_percent': cpu_usage_percent,
            'memory_usage_percent': memory_usage_perecent,
    }
    logging.info("Publishing metrics..")
    future = producer.send('metrics', data)
    result = future.get(timeout=60)

def main():
    server = os.getenv('KAFKA_SERVER', 'localhost:9092')
    producer = KafkaProducer(bootstrap_servers=server, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    logging.info("Obtained connection to Kafka broker")
    
    def handle_signals(signum, frame):
        print('Received signal: ', signum)
        producer.flush()
        producer.close()

    signal.signal(signal.SIGINT, handle_signals)
    
    while True:
        publish_metrics(producer)
        time.sleep(10)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()

