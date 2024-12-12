import unittest
from src.pedido import Pedido

class TestPedido(unittest.TestCase):
    def test_creacion_pedido(self):
        """
        Verifica que se pueda crear un pedido con un ID y productos.
        """
        pedido = Pedido("1234", {"Papas Fritas": 2, "Bebida": 1})
        self.assertEqual(pedido.pedido_id, "1234")
        self.assertEqual(pedido.items, {"Papas Fritas": 2, "Bebida": 1})
        self.assertEqual(pedido.estado, Pedido.ESTADO_PENDIENTE)

    def test_actualizar_estado(self):
        """
        Verifica que se pueda actualizar el estado del pedido.
        """
        pedido = Pedido("1234", {"Papas Fritas": 2})
        pedido.estado = Pedido.ESTADO_COMPLETADO
        self.assertEqual(pedido.estado, Pedido.ESTADO_COMPLETADO)
