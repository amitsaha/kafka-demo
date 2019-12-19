from kafka import KafkaConsumer
import psycopg2

import os
import signal
import json
import logging


def store_db(db, data):
    table_name = os.getenv("DB_TABLE_NAME", "node_metrics")

    print("Storing:", data)
    sql = "INSERT INTO {0}(node_id, cpu_usage_percentage, memory_usage_percentage,timestamp) VALUES(%s,%s,%s,%s)".format(
        table_name
    )
    try:
        cur = db.cursor()
        cur.execute(
            sql,
            (
                data["node_id"],
                data["cpu_usage_percent"],
                data["memory_usage_percent"],
                data["timestamp"],
            ),
        )
        db.commit()
        cur.close()
    except Exception as e:
        logging.error("Error inserting record into database: %s", e)


def consume_metrics(consumer, db):
    logging.info("Consuming metrics..")
    for msg in consumer:
        try:
            data = json.loads(msg.value)
        except ValueError:
            logging.info("Ignoring msg, since it is not valid JSON")
        else:
            store_db(db, data)


def main():
    server = os.getenv("KAFKA_SERVER", "localhost:9092")
    topic = os.getenv("KAFKA_TOPIC", "metrics")
    # client_id should be set to be some random string that are guarnteed
    # to be unique across consumers
    consumer = KafkaConsumer(topic, bootstrap_servers=server, client_id="client1")
    logging.info("Obtained connection to Kafka broker")

    db_config = {
        "host": os.getenv("DB_SERVER", "127.0.0.1"),
        "database": os.getenv("DB_NAME", "metrics"),
        "user": os.getenv("DB_USER", "consumer"),
        "password": os.getenv("DB_PASS", "consumer"),
    }
    db = psycopg2.connect(**db_config)

    def handle_signals(signum, frame):
        print("Received signal: ", signum)
        consumer.close()
        db.close()

    signal.signal(signal.SIGINT, handle_signals)
    signal.signal(signal.SIGTERM, handle_signals)
    consume_metrics(consumer, db)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
