from django.test import TestCase
from sprint.models import *
import time
from proyecto.models import *


class SprintModelTest(TestCase):
    """
    Clase de Tests del modelo sprint
    """
    def test_creacion(self):
        """
        verifica que los sprints se guarden correctamente en un estado valido
        """
        proyecto = Proyecto(
                nombre="prueba",
                estado="Pendiente",
                descripcion="proyecto de prueba"
                )
        proyecto.save()
        sprint = Sprint(
            nombre="prueba",
            proyecto=proyecto,
            estado='Pendiente',
            dias_laborales=20,
            dias_habiles='1,2,3,4,5'
            )
        self.assertTrue(sprint.validate_test())

    def test_validacion_nombre(self):
        """
        Verifica que la validacion de obligatoriedad del campo nombre se ejecute correctamente
        """
        p = Proyecto()
        sprint = Sprint(
            proyecto=p,
            estado='Pendiente',
            dias_laborales=20,
            dias_habiles='1,2,3,4,5'
        )
        self.assertTrue(sprint.validate_test(), "Debe ingresar el nombre del sprint")

    def test_validacion_proyecto(self):
        """
        Verifica que la validacion de obligatoriedad del campo proyecto se ejecute correctamente
        """
        sprint = Sprint(
            nombre='prueba',
            estado='Pendiente',
            dias_laborales=20,
            dias_habiles='1,2,3,4,5'
        )
        self.assertTrue(sprint.validate_test(), "En sprint debe estar relacionado a un proyecto")

    def test_validacion_dias_laborales(self):
        """
        Verifica que la validacion de obligatoriedad del campo dias laborales se ejecute correctamente
        """
        p = Proyecto()
        sprint = Sprint(
            nombre='prueba',
            proyecto=p,
            estado='Pendiente',
            dias_habiles='1,2,3,4,5'
        )
        self.assertTrue(sprint.validate_test(), "En sprint debe estar relacionado a un proyecto")

    def test_validacion_dias_laborales(self):
        """
        Verifica que la validacion de obligatoriedad del campo dias habiles se ejecute correctamente
        """
        p = Proyecto()
        sprint = Sprint(
            nombre='prueba',
            proyecto=p,
            estado='Pendiente',
            dias_laborales=20
        )
        self.assertTrue(sprint.validate_test(), "Debe ingresar al menos un dia hábil")

    def test_creacionSprint(self):
        sprint = Sprint()
        self.assertIsNotNone(sprint)

    def test_fechasSprint(self):
        sprint = Sprint(nombre='sprint', fecha_inicio='29/09/2021', fecha_fin='27/09/2021')
        fechaInicio = time.strptime(sprint.fecha_inicio, "%d/%m/%Y")
        fechaFin = time.strptime(sprint.fecha_fin, "%d/%m/%Y")
        self.assertLessEqual(fechaInicio, fechaFin, "La Fecha de Inicio de Sprint debe ser menor a la fecha de Fin")

    def test_duracion(self):
        sprint = Sprint(nombre='sprint', fecha_inicio='29/04/2021', fecha_fin='12/04/2021', dias_laborales=200)
        self.assertIs(sprint.dias_laborales, 200)
