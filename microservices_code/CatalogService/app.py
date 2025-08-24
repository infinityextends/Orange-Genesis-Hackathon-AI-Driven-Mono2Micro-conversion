from typing import Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

from models import Category, Product, Item
from database import get_db, engine
import models
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS configuration to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Placeholder functions for responsibilities (implementation details omitted)
def check_inventory(item_id: int) -> bool:
    """Placeholder: Checks if an item is in stock."""
    # In a real implementation, this would query the database
    return True

def update_inventory(item_id: int, quantity_change: int):
    """Placeholder: Updates item inventory."""
    # In a real implementation, this would update the database
    print(f"Inventory updated for item {item_id} by {quantity_change}")
    pass

# --- API Endpoints ---

@app.get("/")
async def read_root():
    return {"message": "Catalog Service is running"}

@app.get("/categories", response_model=List[Category])
async def list_categories(db: Session = Depends(get_db)):
    """Lists all categories."""
    return db.query(models.Category).all()


@app.get("/categories/{category_id}", response_model=Category)
async def get_category(category_id: int, db: Session = Depends(get_db)):
    """Retrieves a specific category by ID."""
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Retrieves a specific product by ID."""
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    """Retrieves a specific item by ID."""
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.get("/products/{product_id}/items", response_model=List[Item])
async def list_product_items(product_id: int, db: Session = Depends(get_db)):
    """Lists all items associated with a specific product."""
    items = db.query(models.Item).filter(models.Item.product_id == product_id).all()
    return items
