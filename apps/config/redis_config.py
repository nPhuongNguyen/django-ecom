from django.core.cache import cache
from apps.logging import logging_log as lg
class RedisService:
    @staticmethod
    def set(key, value, timeout=3600):
        try:
            cache.set(key, value, timeout=timeout)
            return True
        except Exception as e:
            lg.log_error(
                message=f"[REDIS-ERROR] Set key {key}: {e}"
            )
            return False 
    @staticmethod
    def get(key):
        if not key:
            return None
        try:
            return cache.get(key)
        except Exception as e:
            lg.log_error(
                message=f"[REDIS-ERROR] Get key {key}: {e}"
            )
            return None
        
    @staticmethod
    def delete(key):
        try:
            cache.delete(key)
            return True
        except Exception as e:
            lg.log_error(
                message=f"[REDIS][DELETE] key={key} error={e}"
            )
            return False