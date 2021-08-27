from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

ESTADOS_USUARIO = (
    ('Activo', 'Activo'),
    ('Inactivo', 'Inactivo')
)

class Usuario(AbstractUser):
    ''' Implementa la clase de Usuarios, hereda campos de AbstractUser en la que se
    encuentran campos necesarios como Nombre, Apellido, Contraseña, email, '''
    estado = models.CharField(max_length=8, choices=ESTADOS_USUARIO, default='Activo')
    ci = models.CharField(max_length=10)
    telefono= models.CharField(max_length=50)
    direccion = models.CharField(max_length=200)
    descripcion = models.TextField()
    permisos = models.ManyToManyField('rol.Permiso', blank=False)

    def __str__(self):
        return self.username
