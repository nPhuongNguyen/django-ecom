from pydantic import BaseModel

class ProductAttributePydantic(BaseModel):
    product: int
    attributes: list[int]