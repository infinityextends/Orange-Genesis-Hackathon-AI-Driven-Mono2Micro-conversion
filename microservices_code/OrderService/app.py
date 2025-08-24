from fastapi import FastAPI, HTTPException, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated, List
from pydantic import BaseModel
from datetime import datetime

import orders.models as models
import orders.service as service

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# Dependency to mock authentication (replace with actual auth)
async def get_current_user(username: str = "testuser"):
    return {"username": username}


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# --- Order Endpoints ---
@app.post("/orders/")
async def create_order(
    request: Request,
    username: Annotated[str, Form()],
    item_ids: Annotated[str, Form()],
    quantity: Annotated[str, Form()],
    current_user: dict = Depends(get_current_user),
):
    """Creates a new order.  Assumes item_ids and quantities are comma separated."""
    try:
        item_ids_list = [int(item_id) for item_id in item_ids.split(",")]
        quantity_list = [int(qty) for qty in quantity.split(",")]

        # Basic validation (can be improved)
        if len(item_ids_list) != len(quantity_list):
            return templates.TemplateResponse(
                "order_result.html",
                {
                    "request": request,
                    "result": "Error: Number of item IDs and quantities must match.",
                },
            )

        order = service.create_order(
            username=username, item_ids=item_ids_list, quantities=quantity_list
        )  # Call to service layer

        return templates.TemplateResponse(
            "order_result.html",
            {"request": request, "result": f"Order created with ID: {order.order_id}"},
        )
    except ValueError as e:
        return templates.TemplateResponse(
            "order_result.html",
            {"request": request, "result": f"Error: Invalid input. {e}"},
        )
    except Exception as e:
        return templates.TemplateResponse(
            "order_result.html",
            {"request": request, "result": f"Error creating order: {e}"},
        )


@app.get("/orders/", response_model=List[models.Order])
async def list_orders(current_user: dict = Depends(get_current_user)):
    """Retrieves all orders (for now, just placeholder)."""
    orders = service.get_all_orders()
    return orders


@app.get("/orders/{order_id}", response_model=models.Order)
async def get_order(order_id: int, current_user: dict = Depends(get_current_user)):
    """Retrieves an order by its ID."""
    order = service.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.get("/orders/users/{username}", response_model=List[models.Order])
async def get_orders_by_user(username: str, current_user: dict = Depends(get_current_user)):
    """Retrieves orders for a specific user."""
    orders = service.get_orders_by_username(username)
    return orders


@app.get("/ui/orders/", response_class=HTMLResponse)
async def create_order_form(request: Request):
    return templates.TemplateResponse("create_order.html", {"request": request})
