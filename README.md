# Kafka demo

This is a demo repository showing how one can setup a kafka producer and consumer.
The kafka producer publishes some operating system metrics to a Kafka topic, which
the consumer consumes from and inserts into a PostgreSQL database.

## Local Kafka and PostgreSQL setup on Linux

This step is only required if you are setting everything up on your local workstation.
The individual scripts are made available so that you as the reader are aware of the few
things that's going behind the scenes. 

### Kafka

There are a few scripts to help you setup Kafka running locally. You will need Java, tar and wget
installed.

The scripts are available in the [kafka](./kafka) directory:

- Download Kafka using `dl_extract_kafka.sh`
- Start Zookeeper using `start_zk.sh`
- Start Kafka using `start_kafka.sh`
- Create Kafka topic `metrics` using `create_topic.sh`

### PostgreSQL

Setup a local installation of PostgreSQL using the instructions from [here](https://wiki.archlinux.org/index.php/PostgreSQL). 
Your Linux distro may have it's own dedicated installation guide.

## Setup Kafka and PostgreSQL

These steps should be executed after you have got access to a Kafka cluster and a PostgreSQL server.

### Kafka

- Create a topic called "metrics"

### PostgreSQL

Login as the "superuser" and run the following SQL commands interactively (one by one):


```
CREATE DATABASE metrics;
CREATE USER consumer WITH ENCRYPTED PASSWORD 'consumer';
GRANT ALL PRIVILEGES ON DATABASE metrics TO consumer;

\connect  metrics;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO consumer;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO consumer;
CREATE TABLE node_metrics(id serial PRIMARY KEY, node_id VARCHAR(32), cpu_usage_percentage REAL NOT NULL, memory_usage_percentage REAL NOT NULL, timestamp BIGINT NOT NULL);
```

## Producer and Consumer

- [Python](./producer_consumer/python)
