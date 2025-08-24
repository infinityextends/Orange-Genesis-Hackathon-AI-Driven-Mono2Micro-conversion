from fastapi import APIRouter, HTTPException
from models.product import Product
from daos.product_dao import ProductDao
from typing import Optional

router = APIRouter(
    prefix="/products",
    tags=["products"],
)

product_dao = ProductDao()

@router.get("/{product_id}", response_model=Optional[Product])
async def read_product(product_id: int):
    """Retrieve a product by ID."""
    product = product_dao.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
