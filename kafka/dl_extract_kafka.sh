#!/bin/bash

set -e
wget http://apache.mirror.digitalpacific.com.au/kafka/2.4.0/kafka_2.12-2.4.0.tgz
tar -zxvf kafka_2.12-2.4.0.tgz
rm kafka_2.12-2.4.0.tgz

