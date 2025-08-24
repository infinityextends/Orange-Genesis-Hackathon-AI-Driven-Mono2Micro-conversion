from fastapi import APIRouter, HTTPException
from typing import Optional

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    responses={404: {"description": "Not found"}},
)

# Placeholder data (replace with database interaction later)
categories_db = {
    "1": {"id": "1", "name": "Electronics"},
    "2": {"id": "2", "name": "Books"},
}

@router.get("/")
async def read_categories():
    """
    Retrieve all categories.
    """
    return list(categories_db.values())

@router.get("/{category_id}")
async def read_category(category_id: str):
    """
    Retrieve a category by its ID.
    """
    if category_id not in categories_db:
        raise HTTPException(status_code=404, detail="Category not found")
    return categories_db[category_id]

# Placeholder function (replace with actual implementation)
def create_category(category_data: dict):
  """
  Creates a new category.
  """
  # TODO: Implement category creation logic.
  pass

def update_category(category_id: str, category_data: dict):
  """
  Updates an existing category.
  """
  # TODO: Implement category update logic.
  pass

def delete_category(category_id: str: str):
  """
  Deletes a category.
  """
  # TODO: Implement category deletion logic.
  pass
