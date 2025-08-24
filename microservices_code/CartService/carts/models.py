from typing import Optional
from typing import List, Optional
from pydantic import BaseModel

class CartItem(BaseModel):
    item_id: str
    quantity: int
    price: float
    name: str
    description: str
    image_url: str

class Cart(BaseModel):
    user_id: str
    items: List[CartItem] = []
    total: float = 0.0
