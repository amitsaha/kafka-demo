from kafka import KafkaConsumer

import os
import signal
import json
import logging

def consume_metrics(consumer):
    logging.info("Consuming metrics..")
    for msg in consumer:
        print(msg)

def main():
    server = os.getenv('KAFKA_SERVER', 'localhost:9092')
    consumer = KafkaConsumer('metrics', bootstrap_servers=server)
    logging.info("Obtained connection to Kafka broker")
    
    def handle_signals(signum, frame):
        print('Received signal: ', signum)
        consumer.close()

    signal.signal(signal.SIGINT, handle_signals)
    signal.signal(signal.SIGTERM, handle_signals)
    consume_metrics(consumer)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()

