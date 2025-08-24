from fastapi import APIRouter, HTTPException
from typing import List
from .models import Cart, CartItem
from .services import cart_service

router = APIRouter(prefix="/carts", tags=["carts"])


@router.get("/{user_id}", response_model=Cart)
async def get_cart(user_id: str):
    """
    Retrieve a user's cart.
    """
    cart = cart_service.get_cart(user_id)
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart

@router.post("/{user_id}/items", response_model=Cart)
async def add_item_to_cart(user_id: str, item: CartItem):
    """
    Add an item to the user's cart.
    """
    try:
        return cart_service.add_item_to_cart(user_id, item)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{user_id}/items/{item_id}", response_model=Cart)
async def update_cart_item(user_id: str, item_id: str, quantity: int):
    """
    Update the quantity of an item in the cart.
    """
    try:
        return cart_service.update_cart_item(user_id, item_id, quantity)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{user_id}/items/{item_id}", response_model=Cart)
async def remove_item_from_cart(user_id: str, item_id: str):
    """
    Remove an item from the user's cart.
    """
    try:
        return cart_service.remove_item_from_cart(user_id, item_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
