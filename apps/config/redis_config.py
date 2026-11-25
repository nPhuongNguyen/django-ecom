from django.core.cache import caches
from apps.logging import logging_log as lg
import time

class RedisConnectionError(Exception):
    pass

class RedisOperationError(Exception):
    pass

class RedisService:
    def __init__(self, alias='default'):
        self.alias = alias
    def get_cache(self):
        try:
            return caches[self.alias]
        except Exception as e:
            lg.log_error("[REDIS] Cache alias Error")
            raise RedisConnectionError("[REDIS] Failed to connect to Redis") from e
    def set(self, key, value, timeout=3600):
        try:
            cache = self.get_cache()
            cache.set(key, value, timeout)
            lg.log_info(f"[REDIS] Set key: {key} with timeout: {timeout} seconds")
            return True
        except Exception as e:
            lg.log_error("[REDIS][SET] Error")
            raise RedisOperationError("[REDIS][SET] Failed to set key") from e
        
    def hset(self, name, key, value):
        try:
            cache = self.get_cache()
            cache.client.get_client().hset(name, key, value)
            lg.log_info(f"[REDIS] HSet name: {name}, key: {key}, value: {value}")
            return True
        except Exception as e:
            lg.log_error("[REDIS][HSET] Error")
            raise RedisOperationError("[REDIS][HSET] Failed to set hash key") from e
    def hget(self, name, key):
        try:
            cache = self.get_cache()
            hget_cahe = cache.client.get_client().hget(name, key)
            lg.log_info(f"[REDIS] HGet name: {name}, key: {key}, value: {hget_cahe}")
            return hget_cahe
        except Exception as e:
            lg.log_error("[REDIS][HGET] Error")
            raise RedisOperationError("[REDIS][HGET] Failed to get hash key") from e
        
    def hincrby(self, name, key, amount=1):
        try:
            cache = self.get_cache()
            new_value = cache.client.get_client().hincrby(name, key, amount)
            lg.log_info(f"[REDIS] HIncrBy name: {name}, key: {key}, amount: {amount}, new_value: {new_value}")
            return new_value
        except Exception as e:
            lg.log_error("[REDIS][HINCRBY] Error")
            raise RedisOperationError("[REDIS][HINCRBY] Failed to increment hash key") from e
    
    def hgetall(self, name):
        try:
            cache = self.get_cache()
            data = cache.client.get_client().hgetall(name)
            lg.log_info(f"[REDIS] HGetAll name: {name}, data: {data}")
            return {k.decode(): v.decode() for k, v in data.items()}
        except Exception as e:
            lg.log_error("[REDIS][HGETALL] Error")
            raise RedisOperationError("[REDIS][HGETALL] Failed to get all hash keys") from e
        
    def hdel(self, name, key):
        try:
            cache = self.get_cache()
            cache.client.get_client().hdel(name, key)
            lg.log_info(f"[REDIS] HDel name: {name}, key: {key}")
            return True
        except Exception as e:
            lg.log_error("[REDIS][HDEL] Error")
            raise RedisOperationError("[REDIS][HDEL] Failed to delete hash key") from e
        
    def get(self, key):
        cache = self.get_cache()
        try:
            return cache.get(key)
        except Exception as e:
            lg.log_error("[REDIS][GET] Error")
            raise RedisOperationError("[REDIS][GET] Failed to get key") from e
        
    def delete(self, key):
        try:
            cache = self.get_cache()
            cache.delete(key)
            return True
        except Exception as e:
            lg.log_error(
                message="[REDIS][DELETE] Error"
            )
            raise RedisOperationError("[REDIS][DELETE] Failed to delete key") from e

    def ping(self, alias="default") -> str:
        try:
            start_time = time.perf_counter()
            cache = self.get_cache(alias)
            if not cache or not cache.client.get_client().ping():
                return "CRITICAL"
            return "WARNING" if (time.perf_counter() - start_time) > 3 else "NORMAL"
        except Exception as e:
            lg.log_error(message=f"[REDIS][PING][{alias}]")
            return "CRITICAL"
        
    def rate_limit(self, key: str, limit: int, window: int) -> bool:
        try:
            cache = self.get_cache()
            client = cache.client.get_client()
            current = client.incr(key)
            if current == 1:
                client.expire(key, window)
            return current <= limit
        except Exception as e:
            lg.log_error(message=f"[REDIS][RATE_LIMIT] Error")
            raise RedisOperationError("[REDIS][RATE_LIMIT] Failed to apply rate limit") from e
        
redis_auth = RedisService(alias="auth")
redis_default = RedisService(alias="default")
