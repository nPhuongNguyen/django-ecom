

from apps.sales.pydantic.order import OrderPydantic
from apps.sales.repositories.order import order_repository

class OrderService:

    def create_order(self, order_data):
        data_input_safe = OrderPydantic(**order_data)
        data_safe_order = {
            "user_id": data_input_safe.user_id,
            "note": data_input_safe.note,
            "total_amount": data_input_safe.total_amount,
            "subtotal_amount": data_input_safe.subtotal_amount,
            "discount_amount": data_input_safe.discount_amount,
        }
        data_safe_order_item = data_input_safe.items
        return order_repository.create_order(data_safe_order, data_safe_order_item)
        
        
oreder_service = OrderService()