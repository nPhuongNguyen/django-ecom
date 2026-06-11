from pydantic import BaseModel

class CartItemPydantic(BaseModel):
    product_variant_id: int
    quantity: int
    
class CartDetailPydantic(BaseModel):
    items: list[CartItemPydantic]