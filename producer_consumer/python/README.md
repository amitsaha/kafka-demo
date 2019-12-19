# Example producer and consumer in Python

The producer and consumer uses [kafka-python](https://github.com/dpkp/kafka-python) package for
communicating with Kafka and [psutil](https://psutil.readthedocs.io/en/latest/) for retrieving
system metrics (producer only). 

[poetry](https://python-poetry.org/) is used for package management.

## Python version and OS dependency

Both the producer and the consumer has been tested with Python 3.7 on Linux only

## Running

Install `poetry`.

### Producer

The "metrics" producer currently publishes the following metrics:

- Percentage CPU usage
- Percentage memory usage

Each metric is augmented by a node identifer and a Unix timestamp. The message
published to the Kafka topic is a serialized JSON message, like so:

```
data = {
        "node_id": "node123",
        "cpu_usage_percent": 1.1,
        "memory_usage_percent": 26.5,
        "timestamp": 1121212121,
}
  
```

The producer recognizes the following environment variables:

- `KAFKA_SERVER`: Bootstrap Kafka server, defaults to `localhost:9092`
- `KAFKA_TOPIC`: Existing Kafka topic to publish metrics to, defaults to `metrics`

To run the producer:

```
$ cd producer
$ poetry run python producer/metrics.py
```

To run unit tests:

```
$ cd producer
$ poetry run pytest
```


### Consumer

The consumer recognizes the following environment variables:

- `KAFKA_SERVER`: Bootstrap Kafka server, defaults to `localhost:9092`
- `KAFKA_TOPIC`: Kafka topic to consume metrics from, defaults to `metrics`
- `DB_TABLE_NAME`: Existing PostgreSQL table name to insert the metrics to, defaults to `node_metrics`
- `DB_SERVER`: PostgreSQL server, defaults to `localhost`
- `DB_NAME`: PostgreSQL database to connect to, defaults to `metrics`
- `DB_USER`: PostgreSQL user to connect to as, defaults to `consumer`
- `DB_PASS`: PostgreSQL user password to, defaults to `consumer`

To run the consumer:

```
$ cd consumer
$ poetry run python consumer/consumer.py
```
To run unit tests:

```
$ cd consumer 
$ poetry run pytest
```



