
from apps.sales.pydantic.cart import CartDetailPydantic, CartItemPydantic
from apps.sales.repositories.cart import cart_repository
from apps.sales.serializers.cart import CartItemSerializer

class CartService:    
    def add_to_cart(self, email, cart_data):
        cart_data = CartItemSerializer(data=cart_data)
        cart_data.is_valid(raise_exception=True)
        cart_data = cart_data.validated_data
        return cart_repository.add_to_cart(email, cart_data)

    def get_cart(self, email):
        cart_data = cart_repository.get_cart(email)
        return CartDetailPydantic(
            items=[
                CartItemPydantic(
                    product_variant_id=int(product_id),
                    quantity=int(quantity)
                )
                for product_id, quantity in cart_data.items()
            ]
        )
    
    def update_cart(self, email, cart_data):
        cart_data = CartItemSerializer(data=cart_data)
        cart_data.is_valid(raise_exception=True)
        cart_data = cart_data.validated_data
        return cart_repository.update_cart(email, cart_data)

    def delete_from_cart(self, email, product_variant_id):
        #check tồn tại user
        #check tồn tại product_variant
        return cart_repository.delete_from_cart(email, product_variant_id)

cart_service = CartService()