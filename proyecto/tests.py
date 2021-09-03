import unittest
import time

from proyecto.models import Proyecto
from proyecto.models import Flujo
from proyecto.models import Fase

class Test(unittest.TestCase):
    """
        Test Creacion de Proyecto
    """
    def test_creacionProyecto(self):
        project = Proyecto()
        self.assertIsNotNone(project)
    """
        Test validacion de fechas de inicio y fin de proyecto
    """
    def test_fechasProyecto(self):
        proyectoPrueba = Proyecto(nombre='ProyectoPrueba', fecha_inicio='21/09/2021', fecha_fin='22/10/2021')
        fechaInicio = time.strptime(proyectoPrueba.fecha_inicio, "%d/%m/%Y")
        fechaFin = time.strptime(proyectoPrueba.fecha_fin, "%d/%m/%Y")
        self.assertLessEqual(fechaInicio, fechaFin, "La Fecha de Inicio debe ser anterior a la fecha de Fin")
    """
        Test Creacion de Flujo
    """
    def test_creacionFlujo(self):
        proyectoPrueba= Proyecto('ProyectoPrueba','21/09/2021','22/10/2021','Pendiente','descripcion')
        flujo= Flujo(proyectoPrueba, 'Flujo', 'desc flujo')
        self.assertIsNotNone(flujo)
    """
        Test Creacion de Fase
    """
    def test_creacionFase(self):
        proyectoPrueba = Proyecto('ProyectoPrueba', '21/09/2021','22/10/2021', 'Pendiente', 'descripcion')
        flujo1 = Flujo(proyectoPrueba, 'Flujo', 'desc flujo')
        fase= Fase(flujo1, 'Fase', 'desc fase')
        self.assertIsNotNone(fase)
