import unittest
from multiprocessing import Manager, Lock
from src.pedido import Pedido
from src.gestor import GestorPedidos
from src.inventario import Inventario
import random
import time
import multiprocessing


class TestGestorPedidos(unittest.TestCase):
    def setUp(self):
        """
        Configuración inicial.
        """
        self.manager = Manager()
        self.lock = Lock()
        self.inventario = Inventario()
        self.gestor = GestorPedidos(self.manager)

    def generar_pedido_aleatorio(self):
        """
        Genera un pedido aleatorio con productos y cantidades.
        """
        platos = list(self.inventario.platos.keys())
        items = {}
        for _ in range(random.randint(1, 4)):  # De 1 a 4 platos por pedido
            plato = random.choice(platos)
            cantidad = random.randint(1, 3)  # Cantidad de 1 a 3 por plato
            if plato in items:
                items[plato] += cantidad
            else:
                items[plato] = cantidad
        return Pedido(str(random.randint(1000, 9999)), items)

    def test_simulacion_masiva(self):
        """
        Prueba una simulación masiva de 10 pedidos procesados en paralelo.
        """
        num_pedidos = 10
        pedidos = [self.generar_pedido_aleatorio() for _ in range(num_pedidos)]

        # Agregar los pedidos al gestor
        for pedido in pedidos:
            self.gestor.recibir_pedido(pedido)

        # Procesar los pedidos
        procesos = []
        inicio = time.time()
        for _ in range(4):  # Procesar con 4 procesos en paralelo
            proceso = multiprocessing.Process(
                target=self.gestor.procesar_pedido,
                args=(self.inventario, self.lock)
            )
            procesos.append(proceso)
            proceso.start()

        for proceso in procesos:
            proceso.join()

        fin = time.time()

        # Validar resultados
        completados = len(self.gestor.pedidos_completados)
        no_procesados = len(self.gestor.pedidos_no_procesados)

        print("\n=== INFORME FINAL ===")
        print(f"Total de pedidos generados: {num_pedidos}")
        print(f"Pedidos completados: {completados}")
        print(f"Pedidos no procesados: {no_procesados}")
        print("\nEstado final del inventario:")
        for item, cantidad in self.inventario.consultar_inventario().items():
            print(f"{item}: {cantidad}")
        print(f"\nTiempo total de procesamiento: {fin - inicio:.2f} segundos")

        # Asegurar que se procesaron algunos pedidos
        self.assertGreater(completados, 0)
        self.assertEqual(completados + no_procesados, num_pedidos)
