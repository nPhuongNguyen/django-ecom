
from pydantic import BaseModel

class OrderItemPydantic(BaseModel):
    product_variant_id: int
    quantity: int
    
class OrderPydantic(BaseModel):
    user_id: int
    items: list[OrderItemPydantic]
    note: str = None
    total_amount: int = 0
    subtotal_amount: int = 0
    discount_amount: int = 0
    