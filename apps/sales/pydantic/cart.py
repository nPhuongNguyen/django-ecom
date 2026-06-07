from pydantic import BaseModel

class ItemPydantic(BaseModel):
    product_variant_id: int
    quantity: int
class CartPydantic(BaseModel):
    user_id: int
    items: list[ItemPydantic]
    
class CartUpdatePydantic(BaseModel):
    items: list[ItemPydantic]