#!/bin/bash

# Run Kafka Server
cd /opt/Kafka/kafka_2.11-1.1.0/
nohup bin/zookeeper-server-start.sh config/zookeeper.properties > /dev/null 2>&1 &
sleep 2
echo "Zookeeper Running..."
nohup bin/kafka-server-start.sh config/server.properties > /dev/null 2>&1 &
sleep 2
echo "Kafka Running..."

# Only run this once.
#bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic jobs
