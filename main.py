from src.menu import Menu
from src.inventario import Inventario

def main():
    print("=== SISTEMA DE GESTIÓN DE PEDIDOS ===")
    print("Simulación de un restaurante usando procesamiento paralelo.\n")
    
    # Crear una instancia única del inventario
    inventario = Inventario()
    
    # Instancia del menú principal
    menu = Menu(inventario)
    menu.mostrar_menu()

if __name__ == "__main__":
    main()
