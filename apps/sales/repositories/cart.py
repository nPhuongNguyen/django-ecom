
from apps.sales.pydantic.cart import CartItemPydantic
from apps.config.redis_config import redis_default

class CartRepository:
    
    def add_to_cart(self, email, cart_data):
        cart_data = CartItemPydantic(**cart_data)
        return redis_default.hincrby(
            f"cart:{email}",
            cart_data.product_variant_id,
            cart_data.quantity
        )
    
    def get_cart(self, email):
        cart_data = redis_default.hgetall(f"cart:{email}")
        return cart_data

    def update_cart(self, email, cart_data):
        cart_data = CartItemPydantic(**cart_data)
        return redis_default.hset(
            f"cart:{email}", 
            cart_data.product_variant_id, 
            cart_data.quantity
        )

    def delete_from_cart(self, email, product_variant_id):
        return redis_default.hdel(f"cart:{email}", product_variant_id)

cart_repository = CartRepository()