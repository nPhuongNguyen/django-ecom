from django.db import connections

from ...config.kafka_config import KafkaService

from ...config.redis_config import RedisService
from ...utils.minio import S3Minio
from apps.logging import logging_log as lg
import time

def check_database(alias="default") -> bool:
    start_time = time.perf_counter()
    try:
        connections[alias].ensure_connection()
        latency = time.perf_counter() - start_time
        if latency > 5:
            return "WARNING", 
        return "NORMAL"
    except Exception:
        lg.log_info(
            message="Connect DB Error"
        )
        return "CRITICAL"

    
def check_redis(alias="default"):
        return RedisService.ping(alias=alias)

def check_kafka():
    return KafkaService().ping()

def check_minio():
    return S3Minio.ping()

