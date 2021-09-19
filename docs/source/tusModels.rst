Comentarios
============

from django.db import models
from proyecto.models import Proyecto
from flujo.models import Flujo

"""
Definicion del modelo de Tipo de User Story
"""

class TipoUserStory(models.Model):

"""
    Se definen los campos necesarios para el modelo
"""
    nombre = models.CharField(max_length=20, blank=False, null=False)
    descripcion = models.TextField(null=True, blank=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, blank=False, null=False)
    flujos = models.ManyToManyField(Flujo, blank=False)