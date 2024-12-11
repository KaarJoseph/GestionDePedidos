import unittest
from src.pedido import Pedido

class TestPedido(unittest.TestCase):
    def test_crear_pedido(self):
        pedido = Pedido("1234", {"pan": 2, "queso": 1})
        self.assertEqual(pedido.pedido_id, "1234")
        self.assertEqual(pedido.items, {"pan": 2, "queso": 1})
        self.assertEqual(pedido.estado, "pendiente")

    def test_estado_pedido(self):
        pedido = Pedido("5678", {"papas": 3})
        pedido.estado = "en preparación"
        self.assertEqual(pedido.estado, "en preparación")

if __name__ == "__main__":
    unittest.main()
