

from pydantic import BaseModel


class OrderItem(BaseModel):
    order_id: int
    product_variant_id: int
    quantity: int