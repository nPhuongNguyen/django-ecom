
from apps.sales.pydantic.cart import CartPydantic, CartUpdatePydantic
from apps.config.redis_config import redis_default

class CartRepository:
    
    def add_to_cart(self, cart_data: CartPydantic):
        add_cart_to_redis = redis_default.hset("cart", cart_data.user_id, cart_data.model_dump_json())
        if not add_cart_to_redis:
            return None
        return cart_data
    
    def get_cart(self, user_id):
        cart_data = redis_default.hget("cart", user_id)
        if not cart_data:
            return None
        return CartPydantic.model_validate_json(cart_data)

    def update_cart(self, user_id, cart_data: CartUpdatePydantic):
        update_cart_in_redis = redis_default.hset("cart", user_id, cart_data.model_dump_json())
        if not update_cart_in_redis:
            return None
        return user_id

cart_repository = CartRepository()