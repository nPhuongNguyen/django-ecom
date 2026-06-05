

from apps.config.redis_config import RedisService
from apps.sales.pydantic.cart import CartPydantic


class CartRepository:
    def __init__(self):
        self.redis = RedisService(alias="default")

    def add_to_cart(self, cart_data):
        cart_data = CartPydantic(**cart_data)
        add_cart_to_redis = self.redis.hset("cart", cart_data.user_id, cart_data.model_dump_json())
        if not add_cart_to_redis:
            return None
        return cart_data