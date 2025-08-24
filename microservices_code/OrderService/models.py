from typing import Optional
from typing import List, Optional
from pydantic import BaseModel

class LineItem(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float

class Order(BaseModel):
    id: int
    customer_id: int
    line_items: List[LineItem]
    total_amount: float
    status: str

class CartItem(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float

class Cart(BaseModel):
    id: int
    customer_id: int
    items: List[CartItem]
    total_amount: float
