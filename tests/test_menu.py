import unittest
from unittest.mock import patch
from multiprocessing import Manager
from src.menu import Menu
from src.inventario import Inventario
from src.gestor import GestorPedidos
from src.pedido import Pedido

class TestMenu(unittest.TestCase):
    def setUp(self):
        """
        Configuración inicial para el menú.
        """
        self.manager = Manager()
        self.inventario = Inventario()
        self.menu = Menu(self.inventario, self.manager)

    @patch('builtins.print')
    @patch('builtins.input', side_effect=["Papas Fritas", "2", "fin"])
    def test_agregar_pedido(self, mock_input, mock_print):
        """
        Prueba la función de agregar pedido.
        """
        self.menu.agregar_pedido()
        # Validar que se agregó el pedido
        self.assertEqual(len(self.menu.gestor.pedidos), 1)
        # Ajusta el mensaje según lo que realmente imprime tu código
        mock_print.assert_any_call("Pedido creado correctamente.")

    @patch('builtins.print')
    @patch('builtins.input', side_effect=["2"])
    def test_procesar_pedidos(self, mock_input, mock_print):
        """
        Prueba el procesamiento de pedidos desde el menú.
        """
        pedido = Pedido("1234", {"Papas Fritas": 2})
        self.menu.gestor.recibir_pedido(pedido)
        self.menu.procesar_pedidos()
        # Validar que el estado cambió a completado
        pedido_procesado = self.menu.gestor.pedidos_completados[0]
        self.assertEqual(pedido_procesado.estado, Pedido.ESTADO_COMPLETADO)

    @patch('builtins.print')
    def test_ver_pedidos(self, mock_print):
        """
        Prueba que los pedidos registrados se muestren correctamente desde el menú.
        """
        pedido = Pedido("1234", {"Papas Fritas": 2})
        self.menu.gestor.recibir_pedido(pedido)
        self.menu.ver_pedidos()
        # Validar que el pedido sea mostrado correctamente
        mock_print.assert_any_call(str(pedido))
