from typing import Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List, Optional
from pydantic import BaseModel
from fastapi import Request

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Mock Catalog Service (replace with actual CatalogService interaction)
class CatalogItem(BaseModel):
    item_id: str
    name: str
    price: float

async def get_catalog_item(item_id: str) -> CatalogItem:
    # Placeholder: In reality, fetch from CatalogService
    if item_id == "123":
        return CatalogItem(item_id="123", name="Test Item", price=10.0)
    else:
        raise HTTPException(status_code=404, detail="Item not found in Catalog")

# Data Models
class CartItem(BaseModel):
    item_id: str
    quantity: int

class Cart(BaseModel):
    user_id: str
    items: List[CartItem] = []

# In-memory cart storage (replace with a database in a real application)
carts = {}

# Utility Functions (Responsibilities as placeholders)
async def calculate_cart_total(cart: Cart) -> float:
    """Calculates the total value of the cart."""
    total = 0.0
    for item in cart.items:
        try:
            catalog_item = await get_catalog_item(item.item_id) #Access the catalog service here
            total += catalog_item.price * item.quantity
        except HTTPException as e:
            raise HTTPException(status_code=404, detail=f"Item {item.item_id} not found in catalog") from e
    return total

async def add_item_to_cart(user_id: str, item_id: str, quantity: int) -> Cart:
    """Adds an item to the user's cart."""
    try:
        await get_catalog_item(item_id) # Check if item exists in catalog
    except HTTPException:
        raise HTTPException(status_code=404, detail="Item not found in catalog")

    if user_id not in carts:
        carts[user_id] = Cart(user_id=user_id, items=[])

    cart = carts[user_id]
    for cart_item in cart.items:
        if cart_item.item_id == item_id:
            cart_item.quantity += quantity
            return cart
    cart.items.append(CartItem(item_id=item_id, quantity=quantity))
    return cart

async def remove_item_from_cart(user_id: str, item_id: str) -> Cart:
    """Removes an item from the user's cart."""
    if user_id not in carts:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart = carts[user_id]
    cart.items = [item for item in cart.items if item.item_id != item_id]
    return cart

async def update_item_quantity(user_id: str, item_id: str, quantity: int) -> Cart:
    """Updates the quantity of an item in the user's cart."""
    if user_id not in carts:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart = carts[user_id]
    for cart_item in cart.items:
        if cart_item.item_id == item_id:
            cart_item.quantity = quantity
            return cart

    raise HTTPException(status_code=404, detail="Item not found in cart")

async def get_cart(user_id: str) -> Cart:
    """Retrieves the user's cart."""
    if user_id not in carts:
        carts[user_id] = Cart(user_id=user_id, items=[])  # Initialize empty cart

    return carts[user_id]

# API Endpoints
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/carts/{user_id}", response_model=Cart)
async def read_cart(user_id: str):
    """Retrieves a user's cart."""
    return await get_cart(user_id)

@app.post("/carts/{user_id}/items", response_model=Cart)
async def add_item(user_id: str, item_id: str, quantity: int):
    """Adds an item to the cart."""
    return await add_item_to_cart(user_id, item_id, quantity)

@app.delete("/carts/{user_id}/items/{item_id}", response_model=Cart)
async def remove_item(user_id: str, item_id: str):
    """Removes an item from the cart."""
    return await remove_item_from_cart(user_id, item_id)

@app.put("/carts/{user_id}/items/{item_id}", response_model=Cart)
async def update_item(user_id: str, item_id: str, quantity: int):
    """Updates the quantity of an item in the cart."""
    return await update_item_quantity(user_id, item_id, quantity)

@app.get("/carts/{user_id}/total")
async def get_cart_total(user_id: str):
    """Calculates the total value of the cart."""
    try:
        cart = await get_cart(user_id)
        total = await calculate_cart_total(cart)
        return {"total": total}
    except HTTPException as e:
        raise e # Re-raise HTTPExceptions from calculate_cart_total
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
