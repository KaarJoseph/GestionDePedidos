import multiprocessing
import time
import sys
from src.pedido import Pedido


class GestorPedidos:
    """
    Clase que gestiona los pedidos en el restaurante.
    Maneja la cola de pedidos, los pedidos completados y no procesados.
    """
    def __init__(self, manager):
        self.cola_pedidos = multiprocessing.Queue()
        self.pedidos = manager.list()  # Lista compartida para registrar todos los pedidos
        self.pedidos_completados = manager.list()  # Lista compartida para pedidos completados
        self.pedidos_no_procesados = manager.list()  # Lista compartida para pedidos no procesados

    def recibir_pedido(self, pedido):
        """
        Agrega un pedido a la cola y lo registra en la lista de pedidos.
        :param pedido: Objeto Pedido.
        """
        print(f"Recibiendo pedido: {pedido}")
        self.cola_pedidos.put(pedido)
        self.pedidos.append(pedido)

    def procesar_pedido(self, inventario, lock):
        """
        Procesa los pedidos en la cola.
        :param inventario: Objeto Inventario.
        :param lock: Multiprocessing Lock para sincronización.
        """
        while not self.cola_pedidos.empty():
            pedido = self.cola_pedidos.get()
            pedido.estado = Pedido.ESTADO_EN_PREPARACION
            print(f"\nPedido {pedido.pedido_id} está en preparación... Estado actual: {pedido.estado}")

            # Animación de progreso
            for i in range(11):  # Simula progreso del 0% al 100%
                time.sleep(0.3)  # Simula tiempo de procesamiento
                sys.stdout.write(f"\rProgreso Pedido {pedido.pedido_id}: [{'#' * i}{'.' * (10 - i)}] {i * 10}%")
                sys.stdout.flush()

            print(f"\nPedido {pedido.pedido_id} finalizado. Actualizando inventario...")
            with lock:
                if inventario.actualizar_inventario(pedido.items):
                    pedido.estado = Pedido.ESTADO_COMPLETADO
                    self.pedidos_completados.append(pedido)
                    print(f"Pedido {pedido.pedido_id} completado con éxito.")
                else:
                    pedido.estado = Pedido.ESTADO_NO_PROCESADO
                    self.pedidos_no_procesados.append(pedido)
                    print(f"Pedido {pedido.pedido_id} no pudo ser procesado (falta de stock).")

            # Actualizar el estado del pedido en la lista global
            self.actualizar_estado_pedido(pedido)

    def actualizar_estado_pedido(self, pedido_actualizado):
        """
        Actualiza el estado de un pedido en la lista global de pedidos.
        :param pedido_actualizado: Objeto Pedido con el estado actualizado.
        """
        for i, pedido in enumerate(self.pedidos):
            if pedido.pedido_id == pedido_actualizado.pedido_id:
                self.pedidos[i] = pedido_actualizado
                break

    def obtener_pedidos(self):
        """
        Devuelve todos los pedidos registrados.
        :return: Lista de todos los pedidos.
        """
        return list(self.pedidos)

    def reporte_final(self):
        """
        Genera un informe final del estado de los pedidos y el inventario.
        """
        print("\n=== REPORTE FINAL ===")
        print("\nPedidos Completados:")
        if not self.pedidos_completados:
            print("No hay pedidos completados.")
        else:
            for pedido in self.pedidos_completados:
                print(pedido)

        print("\nPedidos No Procesados:")
        if not self.pedidos_no_procesados:
            print("No hay pedidos no procesados.")
        else:
            for pedido in self.pedidos_no_procesados:
                print(pedido)

        print("\nPedidos Pendientes:")
        pendientes = [p for p in self.pedidos if p.estado == Pedido.ESTADO_PENDIENTE]
        if not pendientes:
            print("No hay pedidos pendientes.")
        else:
            for pedido in pendientes:
                print(pedido)
