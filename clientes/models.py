from django.db import models
from django.contrib.auth.models import User

"""
Definicion del modelo Cliente
"""
class Cliente(models.Model):
    """
    Implementa la clase de clientes, con las informaciones generales de los clientes:
    nombre, descripcion, direccion, ruc y telefono
    """
    nombre = models.CharField(max_length=100, blank=False, null=False)
    descripcion = models.TextField(max_length=300, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=False, null=True)
    ruc = models.CharField(max_length=50, blank=False, null=True, unique=True)
    telefono = models.CharField(max_length=30, blank=False, null=False)

    def __str__(self):
        """
        Metodo que retorna el nombre del cliente actual
        :return: retorna el valor del campo nombre del objeto actual
        """
        return self.nombre
