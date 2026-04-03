from django.core.cache import caches
from apps.logging import logging_log as lg
import time
class RedisService:
    def __init__(self, alias='default'):
        self.alias = alias
    def get_cache(self):
        try:
            return caches[self.alias]
        except Exception:
            lg.log_error("[REDIS] Cache alias Error")
            return None
    def set(self, key, value, timeout=3600):
        cache = self.get_cache()
        if not cache:
            lg.log_error("[REDIS] Cache not found")
            return False
        try:
            cache.set(key, value, timeout)
            lg.log_info(f"[REDIS] Set key: {key} with timeout: {timeout} seconds")
            return True
        except Exception:
            lg.log_error("[REDIS][SET] Error")
            return False
        
    def get(self, key):
        cache = self.get_cache()
        if not cache:
            return None
        try:
            return cache.get(key)
        except Exception:
            lg.log_error("[REDIS][GET] Error")
            return None
        
    def delete(self, key):
        cache = self.get_cache()
        if not cache:
            return False
        try:
            cache.delete(key)
            return True
        except Exception:
            lg.log_error(
                message="[REDIS][DELETE] Error"
            )
            return False

    def hset_user(self, user_id, data_dict):
        try:
            cache = self.get_cache()
            if not cache:
                return False
            client = cache.client.get_client()
            client.hset(f"user:{user_id}", mapping=data_dict)
            return True
        except Exception:
            lg.log_error(message="[REDIS-ERROR] HSET Error")
            return False
    def ping(self, alias="default") -> str:
        start_time = time.perf_counter()
        try:
            cache = self.get_cache(alias)
            if not cache or not cache.client.get_client().ping():
                return "CRITICAL"
            return "WARNING" if (time.perf_counter() - start_time) > 3 else "NORMAL"
        except Exception:
            lg.log_error(message=f"[REDIS][PING][{alias}]")
            return "CRITICAL"
        
    def rate_limit(self, key: str, limit: int, window: int) -> bool:
        try:
            cache = self.get_cache()
            if not cache:
                return False

            client = cache.client.get_client()
            current = client.incr(key)
            if current == 1:
                client.expire(key, window)
            return current <= limit
        except Exception:
            lg.log_error(message=f"[REDIS][RATE_LIMIT] Error")
            return False
