from pydantic import BaseModel

class Product(BaseModel):
    productId: str
    categoryId: str
    name: str
    description: str
