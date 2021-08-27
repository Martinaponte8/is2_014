
from django.db import models

# Create your models here.

class Permiso(models.Model):
    '''Define la clase de permisos'''
    nombre = models.CharField(max_length=70, blank=False, null=False)
    ''' tipo 1 = Permisos de administracion
        tipo 2 = Permisos de Proyecto'''
    tipo = models.IntegerField()

    def __str__(self):
        return self.nombre



class Rol(models.Model):
    id = models.AutoField
    nombre = models.CharField(max_length=50, unique=True,blank=False, null=False)
    descripcion = models.CharField(max_length=300)
    permisos = models.ManyToManyField('Permiso', blank=False)

    def __str__(self):
        return self.nombre

    def get_id(self):
        return self.id

    def set_nombre(self,nom):
        self.nombre = nom

    def set_descripcion(self, desc):
        self.descripcion = desc

    def get_descripcion(self):
        return self.descripcion

    def set_permiso(self, permisos):
        self.permisos = permisos

    def get_permiso(self):
        return self.permisos

    def list_permisos(self):
        permisos = self.permiso.filter()
        lista = list(permisos)
        return lista

    def agregar_permiso(self, permiso):
        self.permisos.append(permiso)
