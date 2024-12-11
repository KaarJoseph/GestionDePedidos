import unittest
from unittest.mock import patch
from multiprocessing import Manager
from src.menu import Menu
from src.inventario import Inventario

class TestMenu(unittest.TestCase):
    def setUp(self):
        manager = Manager()
        self.inventario = Inventario()
        self.menu = Menu(self.inventario, manager)

    @patch("builtins.input", side_effect=["pan", "2", "fin"])
    def test_agregar_pedido(self, mock_input):
        self.menu.agregar_pedido()
        pedidos = self.menu.gestor.obtener_pedidos()
        self.assertEqual(len(pedidos), 1)
        self.assertEqual(pedidos[0].items, {"pan": 2})

    @patch("builtins.input", side_effect=["pan", "1000", "fin"])
    def test_agregar_pedido_sin_stock(self, mock_input):
        self.menu.agregar_pedido()
        pedidos = self.menu.gestor.obtener_pedidos()
        self.assertEqual(len(pedidos), 1)
        self.assertEqual(pedidos[0].items, {"pan": 1000})

if __name__ == "__main__":
    unittest.main()
