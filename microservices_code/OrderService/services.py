from typing import List, Dict
from . import models, schemas

# Placeholder data (replace with actual database interactions)
orders = [
    models.Order(id=1, customer_id=101, line_items=[models.LineItem(id=1, product_id=1, quantity=2, price=10.0)], total_amount=20.0, status="Pending"),
    models.Order(id=2, customer_id=102, line_items=[models.LineItem(id=2, product_id=2, quantity=1, price=30.0)], total_amount=30.0, status="Shipped")
]

cart = models.Cart(id=1, customer_id=101, items=[models.CartItem(id=1, product_id=1, quantity=1, price=10.0)], total_amount=10.0)

def list_orders() -> List[schemas.Order]:
    """List all orders."""
    return orders


def get_order(order_id: int) -> schemas.Order:
    """Retrieve an order by ID."""
    for order in orders:
        if order.id == order_id:
            return order
    return None


def process_checkout() -> Dict:
    """Process checkout for the current cart."""
    # Simulate payment processing and order confirmation
    print("Processing payment...")
    print("Sending order confirmation email...")
    # In a real implementation, you would interact with the CatalogService and AccountService here
    return {"message": "Checkout successful!", "order_id": 3, "total_amount": cart.total_amount}


def get_cart() -> schemas.Cart:
    """Retrieve the current cart."""
    return cart


def add_to_cart(item: schemas.CartItemCreate) -> schemas.Cart:
    """Add an item to the cart."""
    # In a real implementation, you would fetch the product details from the CatalogService
    new_item = models.CartItem(id=len(cart.items) + 1, product_id=item.product_id, quantity=item.quantity, price=25.0) #dummy price
    cart.items.append(new_item)
    cart.total_amount += new_item.price * new_item.quantity
    return cart


def remove_from_cart(item_id: int) -> schemas.Cart:
    """Remove an item from the cart."""
    for item in cart.items:
        if item.id == item_id:
            cart.total_amount -= item.price * item.quantity
            cart.items.remove(item)
            return cart
    return cart

def update_cart_item(item_id: int, item_update: schemas.CartItemUpdate) -> schemas.Cart:
    """Update the quantity of an item in the cart."""
    for item in cart.items:
        if item.id == item_id:
            cart.total_amount -= item.price * item.quantity
            item.quantity = item_update.quantity
            cart.total_amount += item.price * item.quantity
            return cart
    return cart
