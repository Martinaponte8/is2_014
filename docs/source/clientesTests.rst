Comentarios
============

import unittest
from clientes.models import Cliente

class Test(unittest.TestCase):
    """
    Test para creacion de cliente
    """
    def test_crearcliente(self):
        cliente1 = Cliente()
        self.assertIsNotNone(cliente1)