from fastapi import APIRouter, HTTPException
from typing import List
from models.category import Category
from daos.category_dao import CategoryDao

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)

category_dao = CategoryDao()

@router.get("", response_model=List[Category])
async def read_categories():
    """Retrieve all categories."""
    return category_dao.get_all_categories()

@router.get("/{category_id}", response_model=Category)
async def read_category(category_id: int):
    """Retrieve a category by ID."""
    category = category_dao.get_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.get("/{category_id}/products")
async def read_category_products(category_id: int):
    """Retrieve products for a specific category ID."""
    product_ids = category_dao.get_products_by_category(category_id)
    return {"product_ids": product_ids}
