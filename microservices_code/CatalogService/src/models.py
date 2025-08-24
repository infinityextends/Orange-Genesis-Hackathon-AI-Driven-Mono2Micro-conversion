from pydantic import BaseModel
from typing import Optional

class Category(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

class Product(BaseModel):
    id: int
    name: str
    category_id: int
    description: Optional[str] = None

class Item(BaseModel):
    id: int
    product_id: int
    sku: str
    price: float
