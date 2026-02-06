from django.db import connections

from ...config.kafka_config import KafkaService

from ...config.redis_config import RedisService
from ...utils.minio import S3Minio

def check_database(alias="default") -> bool:
    try:
        connections[alias].ensure_connection()
        return True
    except Exception:
        return False

    
def check_redis(alias="default")->bool:
        return RedisService.ping(alias=alias)

def check_kafka()-> bool:
    return KafkaService().ping()

def check_minio()-> bool:
    return S3Minio.ping()

