from src.menu import Menu

def main():
    print("=== SISTEMA DE GESTIÓN DE PEDIDOS ===")
    print("Simulación de un restaurante usando procesamiento paralelo.\n")
    
    # Instancia del menú principal
    menu = Menu()
    menu.mostrar_menu()

if __name__ == "__main__":
    main()
