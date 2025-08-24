from pydantic import BaseModel

class Item(BaseModel):
    itemId: str
    productId: str
    description: str
    unitCost: float
