#!/bin/bash
set -e
KAFKA_DIR="./kafka_2.12-2.4.0"
$KAFKA_DIR/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic metrics
