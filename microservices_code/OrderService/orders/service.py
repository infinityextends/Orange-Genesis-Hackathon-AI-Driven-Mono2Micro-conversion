import orders.models as models
from datetime import datetime

# Mock database (replace with actual database integration)
orders_db = {}
next_order_id = 1


def create_order(username: str, item_ids: list[int], quantities: list[int]) -> models.Order:
    """Creates a new order."""
    global next_order_id
    order_id = next_order_id
    next_order_id += 1

    # Mock CatalogService integration (replace with actual call)
    total_amount = 0.0
    line_items = []
    for item_id, quantity in zip(item_ids, quantities):
        # Assume CatalogService returns a price for each item
        # For now, just mock the price
        price = float(item_id * 10)  # Example: Item ID 1 costs 10.0, Item ID 2 costs 20.0, etc.
        line_item = models.LineItem(item_id=item_id, quantity=quantity, price=price)
        line_items.append(line_item)
        total_amount += price * quantity

    order = models.Order(
        order_id=order_id,
        username=username,
        order_date=datetime.now(),
        line_items=line_items,
        total_amount=total_amount,
        status="PENDING",
    )

    orders_db[order_id] = order
    return order


def get_order_by_id(order_id: int) -> models.Order | None:
    """Retrieves an order by its ID."""
    return orders_db.get(order_id)


def get_orders_by_username(username: str) -> list[models.Order]:
    """Retrieves orders for a specific user."""
    return [order for order in orders_db.values() if order.username == username]


def get_all_orders() -> list[models.Order]:
    """Retrieves all orders."""
    return list(orders_db.values())


# --- Placeholder functions for other responsibilities ---
def validate_order(order: models.Order) -> bool:
    """Validates an order (placeholder)."""
    # Implement order validation logic here
    return True


def process_payment(order: models.Order) -> bool:
    """Processes payment for an order (placeholder, mocks payment service)."""
    # Implement payment processing logic (mocked)
    return True


def schedule_shipping(order: models.Order) -> bool:
    """Schedules shipping for an order (placeholder, mocks shipping service)."""
    # Implement shipping scheduling logic (mocked)
    return True
