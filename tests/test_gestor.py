import unittest
from multiprocessing import Manager, Lock
from src.gestor import GestorPedidos
from src.pedido import Pedido
from src.inventario import Inventario

class TestGestorPedidos(unittest.TestCase):
    def setUp(self):
        """
        Configuración inicial de los tests, creando un manager, un lock y las instancias necesarias.
        """
        self.manager = Manager()
        self.lock = Lock()
        self.gestor = GestorPedidos(self.manager)
        self.inventario = Inventario()

    def test_recibir_pedido(self):
        pedido = Pedido("1234", {"pan": 2})
        self.gestor.recibir_pedido(pedido)
        recibido = self.gestor.pedidos[0]

        self.assertEqual(recibido.pedido_id, pedido.pedido_id)
        self.assertEqual(recibido.items, pedido.items)
        self.assertEqual(recibido.estado, pedido.estado)

    def test_procesar_pedido_con_stock(self):
        pedido = Pedido("5678", {"pan": 2})
        self.gestor.recibir_pedido(pedido)
        self.gestor.procesar_pedido(self.inventario, self.lock)
        
        # Verificar que el pedido esté en pedidos_completados basado en su ID
        completados_ids = [p.pedido_id for p in self.gestor.pedidos_completados]
        self.assertIn(pedido.pedido_id, completados_ids)

    def test_procesar_pedido_sin_stock(self):
        pedido = Pedido("5678", {"pan": 1000})
        self.gestor.recibir_pedido(pedido)
        self.gestor.procesar_pedido(self.inventario, self.lock)
        
        # Verificar que el pedido esté en pedidos_no_procesados basado en su ID
        no_procesados_ids = [p.pedido_id for p in self.gestor.pedidos_no_procesados]
        self.assertIn(pedido.pedido_id, no_procesados_ids)

if __name__ == "__main__":
    unittest.main()
