import uuid
from src.pedido import Pedido
from src.gestor import GestorPedidos
from src.inventario import Inventario
import multiprocessing

class Menu:
    def __init__(self, inventario):
        manager = multiprocessing.Manager()
        self.inventario = inventario
        self.gestor = GestorPedidos(manager)
        self.lock = multiprocessing.Lock()
class Menu:
    def __init__(self, inventario, manager):
        """
        Clase que representa el menú principal.
        :param inventario: Objeto Inventario.
        :param manager: Multiprocessing Manager para gestionar listas compartidas.
        """
        self.inventario = inventario
        self.gestor = GestorPedidos(manager)
        self.lock = manager.Lock()
        
    def mostrar_menu(self):
        while True:
            print("\n=== MENÚ PRINCIPAL ===")
            print("1. Agregar Pedido")
            print("2. Procesar Pedidos")
            print("3. Consultar Inventario")
            print("4. Ver Pedidos Procesados")
            print("5. Ver Pedidos No Procesados")
            print("6. Ver Todos los Pedidos")
            print("7. Salir")

            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                self.agregar_pedido()
            elif opcion == "2":
                self.procesar_pedidos()
            elif opcion == "3":
                self.consultar_inventario()
            elif opcion == "4":
                self.ver_pedidos_procesados()
            elif opcion == "5":
                self.ver_pedidos_no_procesados()
            elif opcion == "6":
                self.ver_todos_los_pedidos()
            elif opcion == "7":
                print("Saliendo del sistema.")
                break
            else:
                print("Opción inválida. Intente nuevamente.")

    def agregar_pedido(self):
        print("\n=== AGREGAR PEDIDO ===")
        pedido_id = str(uuid.uuid4())[:8]
        items = {}

        while True:
            item = input("Ingrese un producto (o 'fin' para terminar): ").strip().lower()
            if item == "fin":
                if not items:
                    print("El pedido no puede estar vacío. Intente nuevamente.")
                    continue
                break
            if not self.inventario.existe_producto(item):
                print(f"El producto '{item}' no existe en el inventario.")
                continue

            try:
                cantidad = int(input(f"Ingrese la cantidad de {item}: "))
                if cantidad <= 0:
                    print("La cantidad debe ser un número positivo.")
                    continue
                items[item] = cantidad
            except ValueError:
                print("Cantidad inválida. Intente nuevamente.")
                continue

        pedido = Pedido(pedido_id, items)
        self.gestor.recibir_pedido(pedido)
        print(f"Pedido {pedido_id} creado correctamente.")

    def procesar_pedidos(self):
        print("\n=== PROCESAR PEDIDOS ===")
        procesos = []

        for _ in range(2):  # Número de procesos
            p = multiprocessing.Process(target=self.gestor.procesar_pedido, args=(self.inventario, self.lock))
            procesos.append(p)
            p.start()

        for p in procesos:
            p.join()
        print("Procesamiento completado.")

    def consultar_inventario(self):
        print("\n=== INVENTARIO ===")
        for item, cantidad in self.inventario.consultar_inventario().items():
            print(f"{item}: {cantidad}")

    def ver_pedidos_procesados(self):
        print("\n=== PEDIDOS PROCESADOS ===")
        if not self.gestor.pedidos_completados:
            print("No hay pedidos procesados.")
        else:
            for pedido in self.gestor.pedidos_completados:
                print(pedido)

    def ver_pedidos_no_procesados(self):
        print("\n=== PEDIDOS NO PROCESADOS ===")
        if not self.gestor.pedidos_no_procesados:
            print("No hay pedidos no procesados.")
        else:
            for pedido in self.gestor.pedidos_no_procesados:
                print(pedido)

    def ver_todos_los_pedidos(self):
        print("\n=== TODOS LOS PEDIDOS ===")
        todos_los_pedidos = self.gestor.obtener_pedidos()
        if not todos_los_pedidos:
            print("No hay pedidos registrados.")
        else:
            for pedido in todos_los_pedidos:
                print(pedido)
