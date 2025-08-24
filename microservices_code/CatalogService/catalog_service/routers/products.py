from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

# Placeholder data (replace with database interaction later)
products_db = {
    "1": {"id": "1", "name": "Laptop", "category_id": "1"},
    "2": {"id": "2", "name": "Python Crash Course", "category_id": "2"},
}


@router.get("/{product_id}")
async def read_product(product_id: str):
    """
    Retrieve a product by its ID.
    """
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    return products_db[product_id]

# Placeholder functions (replace with actual implementation)
def create_product(product_data: dict):
  """
  Creates a new product.
  """
  # TODO: Implement product creation logic.
  pass

def update_product(product_id: str, product_data: dict):
  """
  Updates an existing product.
  """
  # TODO: Implement product update logic.
  pass

def delete_product(product_id: str):
  """
  Deletes a product.
  """
  # TODO: Implement product deletion logic.
  pass
