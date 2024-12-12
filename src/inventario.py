from multiprocessing import Manager

class Inventario:
    def __init__(self):
        manager = Manager()
        self.platos = manager.dict({
            "Hamburguesa Clásica": {"pan": 2, "queso": 1, "hamburguesa": 1},
            "Papas Fritas": {"papas": 3},
            "Bebida": {"bebidas": 1},
            "Pizza Margarita": {"queso": 2, "pan": 1},
            "Ensalada César": {"ensalada": 1, "queso": 1, "pan": 1},
            "Sandwich Club": {"pan": 3, "queso": 2, "jamón": 1}
        })
        self.ingredientes = manager.dict({
            "pan": 50,
            "queso": 30,
            "hamburguesa": 20,
            "papas": 40,
            "bebidas": 60,
            "ensalada": 15,
            "jamón": 10
        })

    def existe_plato(self, plato):
        """
        Verifica si un plato existe en el menú.
        """
        return plato in self.platos

    def actualizar_inventario(self, items):
        """
        Verifica y actualiza los ingredientes si hay suficiente stock para cada plato.
        :param items: Diccionario con platos y cantidades.
        :return: True si se pudo procesar, False si falta stock para algún plato.
        """
        # Verificar si hay suficiente stock para cada plato
        for plato, cantidad_platos in items.items():
            if plato not in self.platos:
                return False  # Plato no existe en el menú

            # Verificar los ingredientes necesarios para este plato
            ingredientes_necesarios = self.platos[plato]
            for ingrediente, cantidad_necesaria in ingredientes_necesarios.items():
                if self.ingredientes.get(ingrediente, 0) < cantidad_necesaria * cantidad_platos:
                    return False  # Faltan recursos

        # Reducir inventario si todo está disponible
        for plato, cantidad_platos in items.items():
            ingredientes_necesarios = self.platos[plato]
            for ingrediente, cantidad_necesaria in ingredientes_necesarios.items():
                self.ingredientes[ingrediente] -= cantidad_necesaria * cantidad_platos

        return True

    def consultar_inventario(self):
        """
        Devuelve el estado actual del inventario.
        """
        return dict(self.ingredientes)
