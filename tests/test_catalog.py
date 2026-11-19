import unittest
import os
from app.database import CatalogDatabase

class TestCatalog(unittest.TestCase):
    def setUp(self):
        self.db_path = "test_catalog.db"
        self.db = CatalogDatabase(self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except OSError:
                pass

    def test_add_and_search_products(self):
        self.db.add_product("Mechanical Keyboard", "Electronics", 99.99, 15, "RGB Backlit")
        self.db.add_product("Wireless Mouse", "Electronics", 49.99, 20, "Bluetooth 5.0")
        results = self.db.search_products(category="Electronics")
        self.assertEqual(len(results), 2)
        search_res = self.db.search_products(q="Keyboard")
        self.assertEqual(len(search_res), 1)

    def test_stock_mutation(self):
        p = self.db.add_product("Laptop Stand", "Accessories", 29.99, 5, None)
        updated = self.db.update_stock(p["id"], -2)
        self.assertEqual(updated["stock"], 3)
        # Attempt overselling
        invalid = self.db.update_stock(p["id"], -10)
        self.assertIsNone(invalid)

if __name__ == "__main__":
    unittest.main()
