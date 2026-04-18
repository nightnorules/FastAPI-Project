import redis
import json
import logging
from typing import Any, Optional
from backend.app.core.config import settings

logger = logging.getLogger(__name__)


class RedisCache:
    """Simple Redis cache wrapper"""
    
    def __init__(self, url: str = None):
        try:
            self.redis_client = redis.from_url(
                url or settings.redis_url,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_keepalive=True,
                health_check_interval=30,
            )
            self.redis_client.ping()
            self.is_connected = True
            logger.info("Redis cache connected successfully")
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}. Cache will be disabled")
            self.is_connected = False
            self.redis_client = None
    
    def get(self, key: str) -> Optional[Any]:
        if not self.is_connected:
            return None
        
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.warning(f"Cache get error for key {key}: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        if not self.is_connected:
            return False
        
        try:
            self.redis_client.setex(
                key,
                ttl,
                json.dumps(value, default=str)
            )
            return True
        except Exception as e:
            logger.warning(f"Cache set error for key {key}: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if not self.is_connected:
            return False
        
        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            logger.warning(f"Cache delete error for key {key}: {e}")
            return False
    
    def clear(self) -> bool:
        if not self.is_connected:
            return False
        
        try:
            self.redis_client.flushdb()
            return True
        except Exception as e:
            logger.warning(f"Cache clear error: {e}")
            return False
    
    def close(self):
        if self.redis_client:
            self.redis_client.close()
            self.is_connected = False


cache: RedisCache = None


def get_cache() -> RedisCache:
    global cache
    if cache is None:
        cache = RedisCache()
    return cache
