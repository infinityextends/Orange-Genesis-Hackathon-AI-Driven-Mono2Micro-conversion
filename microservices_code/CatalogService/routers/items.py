from fastapi import APIRouter, HTTPException
from models.item import Item
from daos.item_dao import ItemDao
from typing import Optional

router = APIRouter(
    prefix="/items",
    tags=["items"],
)

item_dao = ItemDao()

@router.get("/{item_id}", response_model=Optional[Item])
async def read_item(item_id: int):
    """Retrieve an item by ID."""
    item = item_dao.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
