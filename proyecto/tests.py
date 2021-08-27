import unittest
import time

from proyecto.models import Proyecto
from proyecto.models import Flujo
from proyecto.models import Fase

class Test(unittest.TestCase):
    """
        Test de Creacion de Proyecto
    """
    def test_creacionProyecto(self):
        project = Proyecto()
        self.assertIsNotNone(project)
    """
        Test de validacion de fechas de inicio y fin de proyecto
    """
    def test_fechasProyecto(self):
        proyecto1 = Proyecto(nombre='Proyecto1', fecha_inicio='23/04/2019', fecha_fin='22/04/2019')
        fechaInicio = time.strptime(proyecto1.fecha_inicio, "%d/%m/%Y")
        fechaFin = time.strptime(proyecto1.fecha_fin, "%d/%m/%Y")
        self.assertLessEqual(fechaInicio, fechaFin, "La Fecha de Inicio debe ser menor a la fecha de Fin")
    """
        Test de Creacion de Flujo
    """
    def test_creacionFlujo(self):
        proyecto1= Proyecto('Proyecto1','23/04/2019','23/04/2019','Pendiente','descripcion1')
        flujo1= Flujo(proyecto1, 'Flujo1', 'desc flujo1')
        self.assertIsNotNone(flujo1)
    """
        Test de Creacion de Fase
    """
    def test_creacionFase(self):
        proyecto1 = Proyecto('Proyecto1', '23/04/2019', '23/04/2019', 'Pendiente', 'descripcion1')
        flujo1 = Flujo(proyecto1, 'Flujo1', 'desc flujo1')
        fase1= Fase(flujo1, 'Fase1', 'desc fase1')
        self.assertIsNotNone(fase1)
