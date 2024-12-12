import uuid
from src.pedido import Pedido
from src.gestor import GestorPedidos
from src.inventario import Inventario
import multiprocessing

class Menu:
    def __init__(self, inventario, manager):
        """
        Clase que representa el menú principal.
        :param inventario: Objeto Inventario.
        :param manager: Multiprocessing Manager para gestionar listas compartidas.
        """
        self.inventario = inventario
        self.gestor = GestorPedidos(manager)
        self.lock = multiprocessing.Lock()

    def mostrar_menu(self):
        while True:
            print("\n=== MENÚ PRINCIPAL ===")
            print("1. Agregar Pedido")
            print("2. Procesar Pedidos")
            print("3. Consultar Inventario")
            print("4. Ver Pedidos")
            print("5. Salir")

            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                self.agregar_pedido()
            elif opcion == "2":
                self.procesar_pedidos()
            elif opcion == "3":
                self.consultar_inventario()
            elif opcion == "4":
                self.ver_pedidos()
            elif opcion == "5":
                print("Saliendo del sistema.")
                break
            else:
                print("Opción inválida. Intente nuevamente.")

    def procesar_pedidos(self):
        print("\n=== PROCESAR PEDIDOS ===")
        if not self.gestor.pedidos:
            print("No hay pedidos pendientes para procesar.")
            return

        procesos = []

        for _ in range(3):  # Tres procesos en paralelo
            p = multiprocessing.Process(target=self.gestor.procesar_pedido, args=(self.inventario, self.lock))
            procesos.append(p)
            p.start()

        for p in procesos:
            p.join()
        print("Procesamiento completado.")

    def agregar_pedido(self):
        print("\n=== AGREGAR PEDIDO ===")
        pedido_id = str(uuid.uuid4())[:8]
        items = {}

        while True:
            plato = input("Ingrese un plato (o 'fin' para terminar): ").strip()
            if plato.lower() == "fin":
                if not items:
                    print("El pedido no puede estar vacío. Intente nuevamente.")
                    continue
                break

            if not self.inventario.existe_plato(plato):
                print(f"El plato '{plato}' no existe en el menú.")
                continue

            try:
                cantidad = int(input(f"Ingrese la cantidad de {plato}: "))
                if cantidad <= 0:
                    print("La cantidad debe ser un número positivo.")
                    continue
                items[plato] = cantidad
            except ValueError:
                print("Cantidad inválida. Intente nuevamente.")
                continue

        pedido = Pedido(pedido_id, items)
        self.gestor.recibir_pedido(pedido)
        print(f"Pedido {pedido_id} creado correctamente.")

    def consultar_inventario(self):
        print("\n=== INVENTARIO ===")
        for item, cantidad in self.inventario.consultar_inventario().items():
            print(f"{item}: {cantidad}")

    def ver_pedidos(self):
        print("\n=== TODOS LOS PEDIDOS ===")
        todos_los_pedidos = self.gestor.obtener_pedidos()
        if not todos_los_pedidos:
            print("No hay pedidos registrados.")
        else:
            for pedido in todos_los_pedidos:
                print(str(pedido))  # Convertir explícitamente a cadena

