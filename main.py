from src.menu import Menu
from src.inventario import Inventario
import multiprocessing

def main():
    print("=== SISTEMA DE GESTIÓN DE PEDIDOS ===")
    print("Simulación de un restaurante usando procesamiento paralelo.\n")

    # Crear el inventario inicial
    inventario = Inventario()

    # Crear el Manager para listas compartidas
    manager = multiprocessing.Manager()

    # Inicializar el menú con el inventario y el Manager
    menu = Menu(inventario, manager)

    # Mostrar el menú principal
    menu.mostrar_menu()

if __name__ == "__main__":
    main()
