#!/bin/bash
set -e
KAFKA_DIR="./kafka_2.12-2.4.0"
$KAFKA_DIR/bin/zookeeper-server-start.sh $KAFKA_DIR/config/zookeeper.properties
