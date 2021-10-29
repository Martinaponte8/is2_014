Comentarios
============

import unittest
from tipoUserStory.models import TipoUserStory
from proyecto.models import Proyecto
from flujo.models import Flujo

class Test(unittest.TestCase):

"""
    Prueba de creacion de Tipo de US
"""
    def test_creacionTipoDeUs(self):
        proyecto1 = Proyecto(nombre='Proyecto1', fecha_inicio='23/04/2019', fecha_fin='22/04/2019')
        flujo1 = Flujo(proyecto1, 'Flujo1', 'desc flujo1')
        tipodeus = TipoUserStory(nombre="tipoDeUs", descripcion="desc tipUS", proyecto=proyecto1)
        self.assertIsNotNone(tipodeus)