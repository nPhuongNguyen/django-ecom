import json
from datetime import datetime
import sys
import traceback
from typing import Any
from confluent_kafka import Producer
from django.conf import settings
from ecom.settings import *

def new_brokers() -> list[str]:
    return ["localhost:29092"]

def send_log_to_kibana(request_id, level, msg, metadata):
    try:
        print("[INFO] Sending log to Kibana... DEBUG")
        brokers_list = new_brokers()
        kafka_conf = {
            "bootstrap.servers": ",".join(brokers_list),
            "linger.ms": 10,
            "queue.buffering.max.messages": 10000
        }
        producer = Producer(kafka_conf)

        payload = {
            "ts": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "service_name": SERVICE_NAME,
            "request_id": request_id,
            "log_level": level,
            "msg": msg,
            "metadata": metadata  
        }

        def delivery_report(err, msg):
            if err is not None:
                print(f"Kibana log delivery failed: {err}")
            else:
                info = f"{msg.topic()} [{msg.partition()}] at offset {msg.offset()}"
                print(f"Kibana log delivered successfully: {info}")

        producer.produce(
            topic=KAFKA_TOPIC,
            key=SERVICE_NAME.encode(),
            value=json.dumps(payload).encode("utf-8"),
            callback=delivery_report
        )
        producer.flush(timeout=3)
    except Exception as e: # pylint: disable=broad-exception-caught
        print(f"[send_log_to_kibana] Failed to send log: {e}")

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

class PushHiEcomLog:
    def __init__(self, message):
        self.message = message
        self.topic_name = settings.HI_ECOM_TOPIC
        self.producer_pool = KafkaProducerPool()
        self.producer_pool.initialize(settings.LIST_BROKERS)
        self.prefix_url = settings.PREFIX_URL

    def run(self):
        with self.producer_pool.get_producer() as producer:
            try:
                value = self.message.to_dict() if hasattr(self.message, "to_dict") else self.message
                producer.send(
                    self.topic_name,
                    key=self.prefix_url,
                    value=value
                ) 
                producer.flush()
            except Exception as e:
                print(f"[CONSOLE-ERROR] PushHiEcomLog: {e}")

def push_logs(msg, caller: Any = None):
    if caller is None:
        _, _, exc_tb = sys.exc_info()
        if exc_tb:
            tb_last = traceback.extract_tb(exc_tb)[-1]
            caller = f"File {tb_last.filename} line {tb_last.lineno}, in {tb_last.name}"
        else:
            # fallback nếu không có exception context
            import inspect
            frame = inspect.stack()[1]
            caller = f"File {frame.filename} line {frame.lineno}, in {frame.function}"
    try:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(msg, BaseException):
            msg = {
                "type": type(msg).__name__,
                "message": str(msg),
                "args": msg.args
            }
        else:
            msg = str(msg)
        my_logs = {
            "service_name": settings.PREFIX_URL,
            "sys_time": now,
            "msg_detail": msg,
            "caller": caller,
        }
        if settings.IS_DEV != "1":
            task = PushHiEcomLog(my_logs)
            task.run()
        print("[CONSOLE-INFO]",now, json.dumps(my_logs))
    except Exception as e:
        log_err = {
            "error": e,
            "caller": caller,
            "msg_detail": msg if msg else None,
        }
        print("[CONSOLE-ERROR] Request Log:", json.dumps(log_err))
