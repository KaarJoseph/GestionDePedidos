class Pedido:
    def __init__(self, pedido_id, items):
        """
        Clase que representa un pedido.
        :param pedido_id: ID único del pedido.
        :param items: Diccionario con los productos y sus cantidades.
        """
        self.pedido_id = pedido_id
        self.items = items  # Ejemplo: {'pan': 2, 'queso': 1}
        self.estado = "pendiente"  # Estados: pendiente, en preparación, completado, no procesado

    def __str__(self):
        """
        Representación del pedido como cadena.
        """
        return f"Pedido(ID: {self.pedido_id}, Items: {self.items}, Estado: {self.estado})"
