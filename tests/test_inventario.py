import unittest
from src.inventario import Inventario
from src.pedido import Pedido


class TestInventario(unittest.TestCase):
    def setUp(self):
        self.inventario = Inventario()

    def test_actualizar_inventario_exito(self):
        """
        Verifica que el inventario se actualice correctamente cuando hay suficiente stock.
        """
        pedido = Pedido("1234", {"Papas Fritas": 2})
        self.assertTrue(self.inventario.actualizar_inventario(pedido.items))
        # Verificar que el inventario haya disminuido
        self.assertEqual(self.inventario.ingredientes["papas"], 34)

    def test_actualizar_inventario_fallo(self):
        """
        Verifica que el inventario no se actualice cuando no hay suficiente stock.
        """
        pedido = Pedido("5678", {"Papas Fritas": 100})  # Cantidad exagerada para simular falta de stock
        self.assertFalse(self.inventario.actualizar_inventario(pedido.items))
        # Verificar que el inventario no haya cambiado
        self.assertEqual(self.inventario.ingredientes["papas"], 40)
