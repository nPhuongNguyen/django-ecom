
from PIL.Image import item

from apps.sales.pydantic.cart import CartDetailPydantic, CartItemPydantic, CartItemStatus, ItemPydantic
from apps.sales.repositories.cart import cart_repository
from apps.sales.serializers.cart import CartItemSerializer
from apps.catalogue.repositories.product_variant import product_variant_repository

class CartService:    
    def add_to_cart(self, email, cart_data):
        cart_data = CartItemSerializer(data=cart_data)
        cart_data.is_valid(raise_exception=True)
        cart_data = cart_data.validated_data
        return cart_repository.add_to_cart(email, cart_data)

    def get_cart(self, email):
        cart_data = cart_repository.get_cart(email)
        list_cart_items = []
        for product_variant_id, quantity in cart_data.items():
            item = ItemPydantic(
                product_variant_id=int(product_variant_id),
                quantity=int(quantity)
            )
            product_variant = product_variant_repository.get_product_variant_by_id(product_variant_id)
            if not product_variant:
                item.status = CartItemStatus.PRODUCT_NOT_FOUND
            else:
                item.name = product_variant.name
                item.img = product_variant.img
                item.price = int(product_variant.price)
                item.stock_qty = int(product_variant.stock_qty)
                if product_variant.stock_qty <= 0:
                    item.status = CartItemStatus.OUT_OF_STOCK
                elif product_variant.stock_qty < item.quantity:
                    item.status = CartItemStatus.INSUFFICIENT_STOCK
                else:
                    item.status = CartItemStatus.AVAILABLE
                    item.is_available = True
            list_cart_items.append(item)

        return CartDetailPydantic(items=list_cart_items)

    def update_cart(self, email, cart_data):
        cart_data = CartItemSerializer(data=cart_data)
        cart_data.is_valid(raise_exception=True)
        cart_data = cart_data.validated_data
        return cart_repository.update_cart(email, cart_data)

    def delete_from_cart(self, email, product_variant_id):
        return cart_repository.delete_from_cart(email, product_variant_id)

cart_service = CartService()