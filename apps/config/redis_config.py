from django.core.cache import caches
from apps.logging import logging_log as lg
class RedisService:
    @staticmethod
    def get_cache(alias="default"):
        try:
            return caches[alias]
        except Exception:
            lg.log_error("[REDIS] Cache alias")
            return None
    @staticmethod
    def set(key, value, timeout=3600,  alias="default"):
        cache = RedisService.get_cache(alias)
        if not cache:
            lg.log_error("[REDIS] Cache not found")
            return False
        try:
            cache.set(key, value, timeout)
            lg.log_info(f"[REDIS] Set key: {key} with timeout: {timeout} seconds")
            return True
        except Exception as e:
            lg.log_error("[REDIS][SET]")
            return False
        
    @staticmethod
    def get(key, alias="default"):
        cache = RedisService.get_cache(alias)
        if not cache:
            return None
        try:
            return cache.get(key)
        except Exception:
            lg.log_error("[REDIS][GET]")
            return None
        
    @staticmethod
    def delete(key, alias="default"):
        cache = RedisService.get_cache(alias)
        if not cache:
            return False
        try:
            cache.delete(key)
            return True
        except Exception:
            lg.log_error(
                message="[REDIS][DELETE]"
            )
            return False

    @staticmethod
    def hset_user(user_id, data_dict, alias="default"):
        try:
            cache = RedisService.get_cache(alias)
            if not cache:
                return False
            client = cache.client.get_client()
            client.hset(f"user:{user_id}", mapping=data_dict)
            return True
        except Exception:
            lg.log_error(message="[REDIS-ERROR] HSET")
            return False
    @staticmethod
    def ping(alias="default") -> bool:
        try:
            cache = RedisService.get_cache(alias)
            if not cache:
                return False

            client = cache.client.get_client()
            return client.ping() is True
        except Exception:
            lg.log_error(message=f"[REDIS][PING]")
            return False
        
    @staticmethod
    def rate_limit(key: str, limit: int, window: int, alias="default") -> bool:
        try:
            cache = RedisService.get_cache(alias)
            if not cache:
                return False

            client = cache.client.get_client()
            current = client.incr(key)
            if current == 1:
                client.expire(key, window)
            return current <= limit
        except Exception:
            lg.log_error(message=f"[REDIS][RATE_LIMIT]")
            return False
