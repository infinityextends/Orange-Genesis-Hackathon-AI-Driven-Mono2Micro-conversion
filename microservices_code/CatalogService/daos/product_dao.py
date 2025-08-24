from models.product import Product
from typing import Optional

# Placeholder - replace with actual database interaction logic
class ProductDao:
    def get_product(self, product_id: int) -> Optional[Product]:
        """Retrieve product from database by ID."""
        # Simulate database lookup
        if product_id == 1:
            return Product(id=1, name="Laptop X1", description="Awesome laptop", category_id=1)
        else:
            return None
