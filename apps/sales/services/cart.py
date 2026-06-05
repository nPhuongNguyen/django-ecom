

from apps.config.redis_config import RedisService
from apps.sales.repositories.cart import CartRepository


class CartService:
    def __init__(self):
        self.cart_repository = CartRepository()
        
    def add_to_cart(self, cart_data):
        return self.cart_repository.add_to_cart(cart_data)
cart_service = CartService()