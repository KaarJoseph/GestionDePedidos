import multiprocessing
import time
import sys
from src.pedido import Pedido


class GestorPedidos:
    """
    Clase que gestiona los pedidos en el restaurante.
    Maneja la cola de pedidos, los pedidos completados y no procesados.
    """
    def __init__(self, manager, inventario):
        self.cola_pedidos = multiprocessing.Queue()
        self.pedidos = manager.list()  # Lista compartida para registrar todos los pedidos
        self.pedidos_completados = manager.list()  # Lista compartida para pedidos completados
        self.pedidos_no_procesados = manager.list()  # Lista compartida para pedidos no procesados
        self.inventario = inventario  # Atributo para almacenar el inventario

    def recibir_pedido(self, pedido):
        """
        Agrega un pedido a la cola y lo registra en la lista de pedidos.
        :param pedido: Objeto Pedido.
        """
        print(f"Recibiendo pedido: {pedido}")
        self.cola_pedidos.put(pedido)
        self.pedidos.append(pedido)

    def procesar_pedido(self, inventario, lock, barrier=None, num_pedidos=None, tiempo_inicio=None, informe_generado=None):
        """
        Procesa los pedidos en la cola y genera el informe final desde el último proceso que pasa la barrera.
        """
        while not self.cola_pedidos.empty():
            pedido = self.cola_pedidos.get()
            pedido.estado = Pedido.ESTADO_EN_PREPARACION
            print(f"\nPedido {pedido.pedido_id} está en preparación... Estado actual: {pedido.estado}")

            # Simular progreso
            for i in range(11):
                time.sleep(0.3)
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

            self.actualizar_estado_pedido(pedido)

        # Sincronización con la barrera
        if barrier:
            print(f"Proceso {multiprocessing.current_process().name} esperando en la barrera...")
            barrier.wait()

            # Generar el informe final desde el último proceso
            with lock:  # Usar el lock para evitar condiciones de carrera
                if not informe_generado.value:  # Verificar si el informe ya se generó
                    informe_generado.value = 1  # Marcar el informe como generado
                    tiempo_total = time.time() - tiempo_inicio
                    self.reporte_final(num_pedidos, tiempo_total)

        # Asegurar que no se impriman mensajes innecesarios después del informe
        if informe_generado and informe_generado.value:
            print(f"Proceso {multiprocessing.current_process().name} completó su ejecución.")



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

    def reporte_final(self, num_pedidos, tiempo_total):
        """
        Genera un informe final del estado de los pedidos y el inventario.
        :param num_pedidos: Total de pedidos generados.
        :param tiempo_total: Tiempo total de procesamiento.
        """
        completados = len(self.pedidos_completados)
        no_procesados = len(self.pedidos_no_procesados)

        print("\n=== INFORME FINAL ===")
        print(f"Total de pedidos generados: {num_pedidos}")
        print(f"Pedidos completados: {completados}")
        print(f"Pedidos no procesados: {no_procesados}")
        print("\nEstado final del inventario:")
        for item, cantidad in self.inventario.consultar_inventario().items():
            print(f"{item}: {cantidad}")
        print(f"\nTiempo total de procesamiento: {tiempo_total:.2f} segundos")

