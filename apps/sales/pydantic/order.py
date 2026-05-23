
from pydantic import BaseModel

class OrderPydantic(BaseModel):
    user_id: int
    items: list
    note: str = None
    total_amount: int = 0
    subtotal_amount: int = 0
    discount_amount: int = 0
    