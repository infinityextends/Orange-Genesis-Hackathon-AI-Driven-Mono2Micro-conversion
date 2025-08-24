from pydantic import BaseModel

class Category(BaseModel):
    categoryId: str
    name: str
    description: str
