class Pedido:
    def __init__(self, pedido_id, items):
        self.pedido_id = pedido_id
        self.items = items
        self.estado = "pendiente"

    def __str__(self):
        return f"Pedido(ID: {self.pedido_id}, Items: {self.items}, Estado: {self.estado})"

    def __eq__(self, other):
        # Comparar pedidos basándose en su ID
        if isinstance(other, Pedido):
            return self.pedido_id == other.pedido_id
        return False

    def __hash__(self):
        # Hacer que los pedidos sean hashables para usarlos en estructuras como conjuntos
        return hash(self.pedido_id)
