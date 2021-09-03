from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

"""
Se definen los estados de un Usuario
"""
ESTADOS_USUARIO = (
    ('Activo', 'Activo'),
    ('Inactivo', 'Inactivo')
)
"""
Definimos el modelo Usuario
"""
class Usuario(AbstractUser):
    ''' Implementa la clase de Usuarios, hereda campos de AbstractUser en la que se
    encuentran campos necesarios como Nombre, Apellido, Contraseña, email, '''
    """
       Se definen los demas campos necesarios para el modelo
       """

    estado = models.CharField(max_length=8, choices=ESTADOS_USUARIO, default='Activo')
    ci = models.CharField(max_length=10)
    telefono= models.CharField(max_length=50)
    direccion = models.CharField(max_length=200)
    descripcion = models.TextField()
    permisos = models.ManyToManyField('rol.Permiso', blank=False)

    def __str__(self):
        return self.username
