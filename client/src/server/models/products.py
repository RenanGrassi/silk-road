from pydantic import BaseModel
from typing import Union


class ProductModel(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    is_active: bool = False


class ProductIdModel(BaseModel):
    product_id: int
