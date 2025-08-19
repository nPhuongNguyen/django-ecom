import json
from datetime import datetime
from confluent_kafka import Producer
from apps.logging import logging as lg
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

        producer.produce(
            topic=KAFKA_TOPIC,
            key=SERVICE_NAME.encode(),
            value=json.dumps(payload).encode("utf-8"),
            callback=delivery_report
        )
        producer.flush(timeout=3)
    except Exception as e:
        print(f"[send_log_to_kibana] Failed to send log: {e}")
