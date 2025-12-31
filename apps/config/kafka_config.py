from contextlib import contextmanager
import json
import uuid

from django.conf import settings
from kafka import KafkaProducer, KafkaConsumer
class KafkaProducerPool:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.producers = {}
            cls._instance.initialized = False
        return cls._instance
    def initialize(self, bootstrap_servers: str):
        if not self.initialized:
            self.bootstrap_servers = bootstrap_servers
            self.initialized = True

    @contextmanager
    def get_producer(self):
        producer = self._get_or_create_producer()
        try:
            yield producer
        finally:
            # Không đóng producer ở đây để tái sử dụng
            pass
    
    def _get_or_create_producer(self) -> KafkaProducer:
        key = tuple(self.bootstrap_servers) if isinstance(self.bootstrap_servers, list) else self.bootstrap_servers
        if key not in self.producers:
            self.producers[key] = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                key_serializer=lambda k: k.encode("utf-8")
            )
        return self.producers[key]
    
    def shutdown(self):
        for producer in self.producers.values():
            producer.close()
        self.producers.clear()

class PushO2mSmartlinkAPILog:
    def __init__(self, message):
        self.message = message
        self.topic_name = settings.KAFKA_TOPIC
        self.producer_pool = KafkaProducerPool()
        self.producer_pool.initialize(settings.LIST_BROKERS)
        self.prefix_url = settings.PREFIX_URL

    def run(self):
        try:
            value = self.message.to_dict() if hasattr(self.message, "to_dict") else self.message
            with self.producer_pool.get_producer() as producer:
                producer.send(
                    self.topic_name,
                    key=self.prefix_url,
                    value=value
                ) 
                producer.flush()
        except Exception as e:
            print(f"[CONSOLE-ERROR] PushO2mSmartlinkAPILog: {e}")


class KafkaConsumerWorker:
    def __init__(self):
        self.consumer = KafkaConsumer(
            settings.KAFKA_TOPIC,
            bootstrap_servers=settings.LIST_BROKERS,
            group_id= settings.KAFKA_GROUP_LOG,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            key_deserializer=lambda k: k.decode('utf-8') if k else None,
            auto_offset_reset='earliest',
            enable_auto_commit=False
        )

    def run(self, process_message_fn):
        try:
            for msg in self.consumer:
                try:
                    process_message_fn(msg.key, msg.value)
                    self.consumer.commit() 
                except Exception as e:
                    print(f"[CONSOLE-ERROR] KafkaConsumerWorker: {e}")
        finally:
            self.consumer.close()