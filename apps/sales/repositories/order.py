
from apps.sales.serializers.order import OrderCreateSerializer
from apps.logging import logging_log as lg

class OrderRepository:

    def perform_create(self, serializer, **kwargs):
        if kwargs:
            return serializer.save(**kwargs)
        return serializer.save()
    
    def create_order(self, order_data, order_item_data):
        serializer = OrderCreateSerializer(data=order_data)
        if not serializer.is_valid():
            lg.log_error(
                message="[VALIDATION_ERROR] Invalid order data",
                data=order_data,
                errors=serializer.errors
            )
            return None
        order = self.perform_create(serializer)
        return order