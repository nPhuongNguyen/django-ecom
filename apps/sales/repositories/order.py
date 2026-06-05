
from django.db import transaction
from apps.sales.pydantic.order import OrderItemPydantic
from apps.sales.serializers.order import OrderCreateSerializer, OrderItemCreateSerializer

class OrderRepository:

    def perform_create(self, serializer, **kwargs):
        if kwargs:
            return serializer.save(**kwargs)
        return serializer.save()
    
    def create_order(self, order_data, order_item_data: list[OrderItemPydantic]):
        with transaction.atomic():
            serializer_order = OrderCreateSerializer(data=order_data)
            serializer_order.is_valid(raise_exception=True)
            order = self.perform_create(serializer_order)
            for item_data in order_item_data:
                data_order_item = {
                    "product_variant_id": item_data.product_variant_id,
                    "quantity": item_data.quantity
                }
                serializer_order_item = OrderItemCreateSerializer(data=data_order_item)
                serializer_order_item.is_valid(raise_exception=True)
                self.perform_create(serializer_order_item, order_id=order.id)
        return order