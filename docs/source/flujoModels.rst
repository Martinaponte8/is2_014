Comentarios
============

from django.db import models

"""Definicion del modelo Flujo
"""
class Flujo(models.Model):
    """
    Se definen los campos necesarios para el modelo Flujo
    """
    proyecto = models.ForeignKey('proyecto.Proyecto', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=20)
    descripcion = models.TextField(blank=True, null=True)

"""Definicion del modelo Fase
"""
class Fase(models.Model):

"""
Se definen los campos necesarios del modelo Fase
"""
    flujo = models.ForeignKey(Flujo, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=20)