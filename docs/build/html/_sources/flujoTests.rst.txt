Comentarios
============

import unittest
from flujo.views import TableroTemplateView
from proyecto.models import Proyecto
from flujo.models import Flujo

class Test(unittest.TestCase):

    def test_creacion_flujo(self):
        flujo = Flujo()
        self.assertIsNotNone(flujo)

    def test_flujo_propio_de_proyecto(self):
        proyecto1 = Proyecto()
        flujo = Flujo(proyecto=proyecto1, nombre="proyecto1", descripcion="descripcion")
        self.assertEquals(proyecto1, flujo.proyecto)

    def test_tablero(self):
        tablero = TableroTemplateView()
        self.assertIsNotNone(tablero)