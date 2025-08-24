from models.item import Item
from typing import Optional

# Placeholder - replace with actual database interaction logic
class ItemDao:
    def get_item(self, item_id: int) -> Optional[Item]:
        """Retrieve item from database by ID."""
        # Simulate database lookup
        if item_id == 101:
            return Item(id=101, name="Laptop", description="High-performance laptop", price=1200.00, product_id=1)
        else:
            return None
