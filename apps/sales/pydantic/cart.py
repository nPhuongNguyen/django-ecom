from pydantic import BaseModel

from enum import Enum

class CartItemStatus(str, Enum):
    PRODUCT_NOT_FOUND = "PRODUCT_NOT_FOUND"
    OUT_OF_STOCK = "OUT_OF_STOCK"
    INSUFFICIENT_STOCK = "INSUFFICIENT_STOCK"
    AVAILABLE = "AVAILABLE"

class CartItemPydantic(BaseModel):
    product_variant_id: int
    quantity: int
    
class ItemPydantic(BaseModel):
    product_variant_id: int
    name: str = None
    img: str = None
    quantity: int
    price: int = None
    stock_qty: int = None
    is_available: bool = False
    status: CartItemStatus = CartItemStatus.AVAILABLE
    
class CartDetailPydantic(BaseModel):
    items: list[ItemPydantic]
    

    