import datetime
from django.db import models
from rol.models import Rol
from usuarios.models import Usuario

# Create your models here.
"""
Definimos los estados de un Proyecto
"""

ESTADOS_PROYECTO = (
    ('Pendiente', 'Pendiente'), # cuando se crea
    ('Activo', 'Activo'), # cuando se inicia
    ('Cancelado','Cancelado'), # cuando se cancela
    ('Terminado', 'Terminado'), # cuando se aprueba uno finalizado
    ('Suspendido', 'Suspendido'), # cuando se inactiva el proyecto
)

class Proyecto(models.Model):
    nombre = models.CharField(max_length=20)
    fecha_inicio = models.DateField('Fecha de Inicio Proyecto')
    fecha_fin = models.DateField('Fecha de Fin Proyecto')
    estado = models.CharField(max_length=25, choices=ESTADOS_PROYECTO, default='PEN')
    descripcion= models.TextField()

    def __str__(self):
        return self.nombre

class ProyectoDetalle(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)

ESTADOS_FASE = (
    ('To Do', 'To Do'), # pendiente
    ('Doing', 'Doing'), # en proceso
    ('Do','Do'), #terminado
)

class Flujo(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=20)
    descripcion = models.TextField()

class Fase(models.Model):
    flujo = models.ForeignKey(Flujo,on_delete=models.CASCADE)
    nombre = models.CharField(max_length=20)
    estado = models.CharField(max_length=25, choices=ESTADOS_FASE, default='To Do')
