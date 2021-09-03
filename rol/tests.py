
from django.test import TestCase
import unittest
from rol.models import Permiso, Rol

# Create your tests here.

class Test(unittest.TestCase):

    """
    Test de creacion de Rol vacio
    """
    def test_creacionRol(self):
        rol = Rol()
        self.assertIsNotNone(rol)
