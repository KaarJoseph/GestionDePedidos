import multiprocessing

class GestorPedidos:
    def __init__(self, manager):
        """
        Clase que gestiona los pedidos utilizando una cola y listas compartidas.
        :param manager: Objeto de multiprocessing.Manager.
        """
        self.cola_pedidos = multiprocessing.Queue()
        self.pedidos_completados = manager.list()  # Lista compartida
        self.pedidos_no_procesados = manager.list()  # Lista compartida

    def recibir_pedido(self, pedido):
        """
        Agrega un pedido a la cola.
        :param pedido: Objeto de la clase Pedido.
        """
        print(f"Recibiendo pedido: {pedido}")
        self.cola_pedidos.put(pedido)

    def procesar_pedido(self, inventario, lock):
        """
        Procesa los pedidos en la cola.
        :param inventario: Objeto de la clase Inventario.
        :param lock: Multiprocessing Lock para sincronización.
        """
        while not self.cola_pedidos.empty():
            pedido = self.cola_pedidos.get()
            pedido.estado = "en preparación"
            print(f"Procesando pedido: {pedido.pedido_id}...")

            with lock:
                if inventario.actualizar_inventario(pedido.items):
                    pedido.estado = "completado"
                    self.pedidos_completados.append(pedido)
                else:
                    pedido.estado = "no procesado"
                    self.pedidos_no_procesados.append(pedido)
