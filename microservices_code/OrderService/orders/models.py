from typing import Optional
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class LineItem(BaseModel):
    item_id: int
    quantity: int
    price: float  # added price

class Order(BaseModel):
    order_id: int
    username: str
    order_date: datetime
    line_items: List[LineItem]
    total_amount: float
    status: str  # e.g., "PENDING", "SHIPPED", "DELIVERED"
