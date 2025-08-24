from typing import Optional
from pydantic import BaseModel
from typing import List, Optional

class Order(BaseModel):
    order_id: int
    user_id: int
    items: List[str]
    total: float
    status: str

class OrderCreate(BaseModel):
    user_id: int
    items: List[str]
    total: float

class OrderUpdate(BaseModel):
    user_id: Optional[int] = None
    items: Optional[List[str]] = None
    total: Optional[float] = None
    status: Optional[str] = None
