
from django.test import TestCase
import unittest
from rol.models import Permiso, Rol

# Create your tests here.

class Test(unittest.TestCase):

    """
    Test de creacion de Rol vacio
    """
    def test_creacionRol(self):
        rol1 = Rol()
        self.assertIsNotNone(rol1)
    """
    Test de creacion de Rol sin asignar permisos
    """
    #def test_creacionRolSinPermisos(self):
    #    permiso1= Permiso(nombre="permiso1")
    #    rol1 = Rol(id= 1, nombre="rol1", descripcion="desc rol1")
    #    rol1.permisos.set(permiso1)
    #    self.assertIsNotNone(rol1.permisos)
