import unittest
from src.inventario import Inventario

class TestInventario(unittest.TestCase):
    def setUp(self):
        self.inventario = Inventario()

    def test_existe_producto(self):
        self.assertTrue(self.inventario.existe_producto("pan"))
        self.assertFalse(self.inventario.existe_producto("chocolate"))

    def test_actualizar_inventario_con_stock(self):
        result = self.inventario.actualizar_inventario({"pan": 2, "queso": 1})
        self.assertTrue(result)
        self.assertEqual(self.inventario.stock["pan"], 48)
        self.assertEqual(self.inventario.stock["queso"], 29)

    def test_actualizar_inventario_sin_stock(self):
        result = self.inventario.actualizar_inventario({"pan": 1000})
        self.assertFalse(result)

    def test_consultar_inventario(self):
        stock = self.inventario.consultar_inventario()
        self.assertIn("pan", stock)
        self.assertIn("queso", stock)

if __name__ == "__main__":
    unittest.main()
