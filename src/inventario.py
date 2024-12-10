class Inventario:
    def __init__(self):
        """
        Inicializa el inventario con valores predeterminados.
        """
        self.stock = {
            "pan": 50,
            "queso": 30,
            "jamón": 25,
            "papas": 40,
            "hamburguesa": 20,
            "bebidas": 60,
            "salsas": 100,
            "ensalada": 15
        }

    def existe_producto(self, producto):
        """
        Verifica si un producto existe en el inventario.
        :param producto: Nombre del producto.
        :return: True si existe, False en caso contrario.
        """
        return producto in self.stock

    def actualizar_inventario(self, items):
        """
        Actualiza el inventario si hay stock suficiente.
        :param items: Diccionario con productos y cantidades.
        :return: True si se pudo procesar, False si falta stock.
        """
        for item, cantidad in items.items():
            if self.stock.get(item, 0) < cantidad:
                return False  # Faltan recursos
        
        # Actualizar inventario si hay suficiente stock
        for item, cantidad in items.items():
            self.stock[item] -= cantidad
        return True

    def consultar_inventario(self):
        """
        Devuelve el inventario actual.
        """
        return self.stock
