from typing import List
from models.order import Order

class OrderService:

    def __init__(self):
        # In a real application, this would connect to a database
        self.orders = {}
        self.next_order_id = 1

    def place_order(self, order: Order) -> Order:
        """Places a new order."""
        order.order_id = self.next_order_id
        self.orders[order.order_id] = order
        self.next_order_id += 1
        # Placeholder for integration with payment processing.
        # Placeholder for sending order confirmation emails.
        print(f"Order placed: {order}")
        return order

    def get_order_by_id(self, order_id: int) -> Order:
        """Retrieves an order by ID."""
        return self.orders.get(order_id)


    def get_all_orders(self) -> List[Order]:
        """Retrieves all orders."""
        return list(self.orders.values())

    def update_order(self, order_id: int, order: Order) -> Order:
         """Updates an existing order."""
         if order_id not in self.orders:
            return None

         order.order_id = order_id  # Ensure ID is consistent
         self.orders[order_id] = order
         print(f"Order updated: {order}")
         return order

    def checkout_order(self, order_id: int):
        """Simulates checking out an order, processing payment, and sending an email."""
        order = self.get_order_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        # Placeholder: Integrate with payment processing here
        print(f"Processing payment for order {order_id}")

        # Placeholder: Send order confirmation email here
        print(f"Sending order confirmation email for order {order_id}")

        order.status = "COMPLETED"
        self.orders[order_id] = order
