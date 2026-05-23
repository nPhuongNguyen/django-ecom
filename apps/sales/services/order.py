

from apps.sales.repositories.order import OrderRepository


class OrderService:
    def __init__(self):
        self.order_repository = OrderRepository()
        
    def create_order(self, order_data, order_item_data):
        return self.order_repository.create_order(order_data, order_item_data)
        
        
oreder_service = OrderService()