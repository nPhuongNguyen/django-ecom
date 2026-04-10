from contextlib import contextmanager
import json
from django.conf import settings
from kafka import KafkaAdminClient, KafkaProducer, KafkaConsumer
from apps.logging import logging_log as lg
import time

class KafkaProducerPool:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._producers = {} 
        return cls._instance

    def _get_or_create_producer(self, broker_list) -> KafkaProducer:
        key = str(broker_list)
        if key not in self._producers:
            self._producers[key] = KafkaProducer(
                bootstrap_servers=broker_list,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                key_serializer=lambda k: k.encode("utf-8"),
                
                #Cấu hình nếu kafka broker yeu cầu xác thực
                security_protocol="SASL_PLAINTEXT",
                sasl_mechanism="PLAIN",
                sasl_plain_username="admin",
                sasl_plain_password="admin-secret",
            )
        return self._producers[key]

    @contextmanager
    def get_producer(self, broker_list):
        producer = self._get_or_create_producer(broker_list)
        try:
            yield producer
        finally:
            pass

class PushO2mSmartlinkAPILog:
    def __init__(self, broker_list, topic):
        self.kafkapool = KafkaProducerPool()
        self.broker_list = broker_list
        self.topic = topic  
    def run(self, key, message):
        value = message.to_dict() if hasattr(message, "to_dict") else message
        with self.kafkapool.get_producer(self.broker_list) as producer:
            producer.send(
                topic=self.topic,
                key=key,
                value=value
            )
            producer.flush() 

class InitBroker:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InitBroker, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.push_log_django_ecom = PushO2mSmartlinkAPILog(
                settings.LIST_BROKERS,
                settings.KAFKA_TOPIC
            )
            self._initialized = True
class KafkaService:
    def __init__(self):
        self.bootstrap_servers = settings.LIST_BROKERS
        self.request_timeout_ms = 2000
    def ping(self):
        start = time.process_time()
        try:
            admin = KafkaAdminClient(
                bootstrap_servers=self.bootstrap_servers,
                request_timeout_ms=self.request_timeout_ms
            )
            admin.describe_cluster()
            admin.close()
            return "WARING" if (time.process_time() - start > 3) else "NORMAL"
        except Exception:
            lg.log_error(message=f"[Kafka][PING] Error")
            return "CRITICAL"
