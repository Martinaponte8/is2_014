Comentarios
============

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from rol.models import *
from proyecto.models import TeamMember


"""
Definicion de los estados de un Usuario
"""

ESTADOS_USUARIO = (
    ('Activo', 'Activo'),
    ('Inactivo', 'Inactivo')
)

"""
Definimos el modelo Usuario
"""
class Usuario(AbstractUser):
"""
    Implementa la clase de Usuarios, hereda campos de AbstractUser en la que se
    encuentran campos necesarios como Nombre, Apellido, Contraseña, email,
"""
"""
    Se definen los demas campos necesarios para el modelo
"""

    def __str__(self):
        return self.username

    def get_nombres_permisos(self, proyecto=None):
        if self.is_superuser:
            for permiso in Permiso.objects.all():
                permisos.append(permiso.nombre)
        else:
            for permiso in self.permisos.all():
                permisos.append(permiso.nombre)
            if proyecto:
                try:
                    team_member = TeamMember.objects.get(proyecto=proyecto, usuario=self.pk)
                    rol_usuario = Rol.objects.get(pk=team_member.rol.pk)
                except:
                    pass
                if rol_usuario:
                    for rol in rol_usuario.permisos.all():
                        permisos.append(rol.nombre)
        return permisos
