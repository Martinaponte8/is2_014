
from django.db import models
from rol.models import Rol


"""
Definimos los estados de un Proyecto
"""
ESTADOS_PROYECTO = (
    ('Pendiente', 'Pendiente'),
    ('Activo', 'Activo'),
    ('Cancelado','Cancelado'),
    ('Terminado', 'Terminado'),
    ('Suspendido', 'Suspendido')
)

class Proyecto(models.Model):
    """
        Implementa la clase de Proyectos, almacena datos generales acerca del proyecto:
        fecha de inicio, fecha fin, nombre, estado y descripcion
        """

    nombre = models.CharField(max_length=20, blank=False, null=False)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=25, choices=ESTADOS_PROYECTO, default='Pendiente')
    descripcion= models.TextField(blank=True, null=True)
    fecha_ini_estimada = models.DateField('Fecha de Inicio Estimada', blank=False, null=False)
    fecha_fin_estimada = models.DateField('Fecha de Fin Estimada', blank=False, null=False)

    def __str__(self):
        """
                Metodo que retorna el nombre del proyecto actual
                :return: retorna el valor del campo nombre del objeto actual
                """

        return self.nombre

class TeamMember(models.Model):
    """
        Implementa la clase de Team Member, el cual es una combinacion de un usuario y un rol
        ligada a un proyecto
        """

    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, null=False, blank=False)
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.PROTECT, blank=False, null=False)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, blank=False, null=False)

