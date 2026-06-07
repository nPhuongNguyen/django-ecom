
from apps.sales.pydantic.cart import CartPydantic, CartUpdatePydantic
from apps.sales.repositories.cart import cart_repository

class CartService:    
    def add_to_cart(self, cart_data):
        cart_data = CartPydantic(**cart_data)
        # Check tồn tại user
        # Check tồn tại product_variant
        return cart_repository.add_to_cart(cart_data)

    def get_cart(self, user_id):
        return cart_repository.get_cart(user_id)

    def update_cart(self, user_id, cart_data):
        #check tồn tại user
        cart_data = CartUpdatePydantic(**cart_data)
        #check tồn tại product_variant
        return cart_repository.update_cart(user_id, cart_data)

cart_service = CartService()