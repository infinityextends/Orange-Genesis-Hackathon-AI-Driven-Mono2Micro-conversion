from typing import Optional
from models.category import Category
from typing import List, Optional

# Placeholder - replace with actual database interaction logic
class CategoryDao:
    def get_all_categories(self) -> List[Category]:
        """Retrieve all categories from database."""
        # Simulate database data
        categories = [
            Category(id=1, name="Electronics", description="Electronic devices"),
            Category(id=2, name="Clothing", description="Apparel"),
        ]
        return categories

    def get_category(self, category_id: int) -> Optional[Category]:
        """Retrieve category from database by ID."""
        # Simulate database lookup
        if category_id == 1:
            return Category(id=1, name="Electronics", description="Electronic devices")
        elif category_id == 2:
            return Category(id=2, name="Clothing", description="Apparel")
        else:
            return None

    def get_products_by_category(self, category_id: int) -> List[int]:
      """Retrieve products from database by category ID."""
      # Simulate products associated with a category
      if category_id == 1:
          return [1,2,3]
      elif category_id == 2:
          return [4,5]
      else:
          return []
