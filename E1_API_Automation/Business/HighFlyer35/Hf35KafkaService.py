#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import json

from E1_API_Automation.Business.Utils.EnvUtils import EnvUtils


class Kafka_producer():
    '''
    use kafka producer
    '''

    def __init__(self, kafkahost, kafkatopic):
        self.kafkaHost = kafkahost
        self.kafkatopic = kafkatopic
        if EnvUtils.is_env_stg_cn():
            self.producer = KafkaProducer(sasl_mechanism="PLAIN", security_protocol='SASL_PLAINTEXT',
                                          sasl_plain_username="ckafka-epk0cfr4#ksd", sasl_plain_password="ksd",
                                          bootstrap_servers=self.kafkaHost, api_version=(0, 10, 0))
        else:
            self.producer = KafkaProducer(bootstrap_servers=self.kafkaHost, api_version=(0, 10, 0))

    def sendjsondata(self, params):
        try:
            parmas_message = json.dumps(params)
            producer = self.producer
            producer.send(self.kafkatopic, parmas_message.encode('utf-8'))
            producer.flush()
        except KafkaError as e:
            print(e)

class Kafka_consumer():
    '''
    use Kafka—python consumer
    '''

    def __init__(self, kafkahost, kafkatopic, groupid):
        self.kafkaHost = kafkahost
        self.kafkatopic = kafkatopic
        self.groupid = groupid
        self.consumer = KafkaConsumer(self.kafkatopic, api_version=(0, 10, 0), auto_offset_reset='earliest')

    def consume_data(self):
        try:
            for message in self.consumer:
                yield message
        except KeyboardInterrupt as e:
            print(e)
