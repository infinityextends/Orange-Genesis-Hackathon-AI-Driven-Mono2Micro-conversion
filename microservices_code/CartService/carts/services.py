from typing import Dict
from .models import Cart, CartItem

# In-memory storage for carts (replace with a database in a real application)
carts: Dict[str, Cart] = {}

class CartService:
    def get_cart(self, user_id: str) -> Cart:
        """Retrieves the cart for a given user."""
        if user_id in carts:
            return carts[user_id]
        else:
            # Create a new cart if one doesn't exist
            cart = Cart(user_id=user_id)
            carts[user_id] = cart
            return cart

    def add_item_to_cart(self, user_id: str, item: CartItem) -> Cart:
        """Adds an item to the user's cart."""
        cart = self.get_cart(user_id)
        cart.items.append(item)
        self.calculate_cart_total(cart)
        return cart

    def update_cart_item(self, user_id: str, item_id: str, quantity: int) -> Cart:
        """Updates the quantity of an item in the user's cart."""
        cart = self.get_cart(user_id)
        for item in cart.items:
            if item.item_id == item_id:
                item.quantity = quantity
                break  # Item found and updated
        self.calculate_cart_total(cart)
        return cart

    def remove_item_from_cart(self, user_id: str, item_id: str) -> Cart:
        """Removes an item from the user's cart."""
        cart = self.get_cart(user_id)
        cart.items = [item for item in cart.items if item.item_id != item_id]
        self.calculate_cart_total(cart)
        return cart

    def calculate_cart_total(self, cart: Cart) -> None:
        """Calculates the total value of the cart."""
        cart.total = sum(item.price * item.quantity for item in cart.items)


cart_service = CartService()
