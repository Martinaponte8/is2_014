Comentarios
============

import unittest
from userstory.models import UserStory, Actividad, Archivo, Nota
from proyecto.models import Proyecto

class Test(unittest.TestCase):

"""
    Test para creacion de US
"""
    def test_creacionUs(self):
        us = UserStory()
        self.assertIsNotNone(us)
"""
    Test de Rango permitido
"""
    def test_Rango(self):
        proyecto1 = Proyecto(nombre='Proyecto1', fecha_inicio='23/04/2019', fecha_fin='22/04/2019')
        us = UserStory(proyecto=proyecto1, nombre="p1", descripcion="desc", fecha_inicio='13/04/2019', duracion_estimada=100, valor_negocio=55)
        self.assertLessEqual(us.valor_negocio, 10, "El valor del Valor de Negocio no debe superar el valor de 10")

    def test_actividad(self):
"""
        test para crear actividades
"""
        :return:
"""
        actividad = Actividad(nombre='Actividad 1', descripcion='desc', duracion='1000')
        self.assertIsNotNone(actividad)

    def test_archivo(self):
"""
        test para crear archivos
"""
        :return:
"""
        archivo = Archivo(titulo='Archivo 1')
        self.assertIsNotNone(archivo)

    def test_nota(self):
"""
        test para crear notas
"""
        :return:
"""
        nota = Nota(nota='Nota 1')
        self.assertIsNotNone(nota)