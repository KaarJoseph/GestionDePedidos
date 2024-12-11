import multiprocessing
import time
import sys

class GestorPedidos:
    def __init__(self, manager):
        self.cola_pedidos = multiprocessing.Queue()
        self.pedidos_completados = manager.list()  # Lista compartida
        self.pedidos_no_procesados = manager.list()  # Lista compartida

    def recibir_pedido(self, pedido):
        print(f"Recibiendo pedido: {pedido}")
        self.cola_pedidos.put(pedido)

    def procesar_pedido(self, inventario, lock):
        while not self.cola_pedidos.empty():
            pedido = self.cola_pedidos.get()
            pedido.estado = "en preparación"
            print(f"\nPedido {pedido.pedido_id} está en preparación...")

            # Animación de progreso
            for i in range(11):  # De 0 a 10 (simula progreso del 0% al 100%)
                time.sleep(0.3)  # Simula tiempo de procesamiento
                sys.stdout.write(f"\rProgreso: [{'#' * i}{'.' * (10 - i)}] {i * 10}%")
                sys.stdout.flush()

            print("\nPedido finalizado. Actualizando inventario...")
            with lock:
                if inventario.actualizar_inventario(pedido.items):
                    pedido.estado = "completado"
                    self.pedidos_completados.append(pedido)
                    print(f"Pedido {pedido.pedido_id} completado con éxito.")
                else:
                    pedido.estado = "no procesado"
                    self.pedidos_no_procesados.append(pedido)
                    print(f"Pedido {pedido.pedido_id} no pudo ser procesado (falta de stock).")
