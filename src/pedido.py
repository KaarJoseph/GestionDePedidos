class Pedido:
    ESTADO_PENDIENTE = "pendiente"
    ESTADO_EN_PREPARACION = "en preparación"
    ESTADO_COMPLETADO = "completado"
    ESTADO_NO_PROCESADO = "no procesado"

    def __init__(self, pedido_id, items):
        self.pedido_id = pedido_id
        self.items = items
        self.estado = self.ESTADO_PENDIENTE

    def __str__(self):
        return f"Pedido(ID: {self.pedido_id}, Items: {self.items}, Estado: {self.estado})"

    def __eq__(self, other):
        if isinstance(other, Pedido):
            return self.pedido_id == other.pedido_id
        return False

    def __hash__(self):
        return hash(self.pedido_id)
