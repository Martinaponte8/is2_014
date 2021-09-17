from django.core.exceptions import ValidationError
from django.db import models
from is2_014 import settings


"""
Definicion de los estados de User Story
"""

PENDIENTE = 2
ASIGNADO = 1
FINALIZADO = 0
ESTADOS_US = (
    (PENDIENTE, 'Pendiente'),
    (ASIGNADO, 'Asignado'),
    (FINALIZADO,'Finalizado')
)

"""
Se definen los estados en fase
"""

ESTADOS_EN_FASE = (
    ('To Do', 'To Do'),
    ('Doing', 'Doing'),
    ('Done', 'Done'),
    ('Control de Calidad', 'Control de Calidad'),
)

"""
Metodo que realiza la validacion del rango permitido para los campos de: Valor de Negocio, Prioridad y Valor tecnico 
"""
def rango(valor):
    """
    Validación de rango permitido
    """
    if valor >10 or valor < 0:
        raise ValidationError('El valor debe estar en 0-10')

"""
Se define el modelo User Story
"""
class UserStory(models.Model):
    """
    Se definen los campos necesarios para el modelo
    """
    sprints_asignados = models.ManyToManyField('sprint.Sprint', blank=True, related_name='userstory_sprint_asignado')
    estado_fase = models.CharField(max_length=30, choices=ESTADOS_EN_FASE, default='To Do')
    flujo = models.ForeignKey('flujo.Flujo', on_delete=models.PROTECT)
    fase = models.ForeignKey('flujo.Fase', on_delete=models.PROTECT, null=True, blank=True)
    proyecto = models.ForeignKey('proyecto.Proyecto', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=300)
    fecha_inicio = models.DateField('Fecha de inicio del User Story', null=True, blank=True)
    duracion_estimada = models.TimeField()
    valor_negocio = models.PositiveIntegerField(validators=[rango])
    prioridad = models.PositiveIntegerField(validators=[rango])
    valor_tecnico = models.PositiveIntegerField(validators=[rango])
    estado = models.PositiveIntegerField(default=PENDIENTE, choices=ESTADOS_US)
    team_member = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE, blank=True, null=True)
    tipo_us = models.ForeignKey('tipoUserStory.TipoUserStory', on_delete=models.PROTECT)
    sprint = models.ForeignKey('sprint.Sprint', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.nombre

    def set_priorizacion(self):
        return (2*self.valor_negocio + self.prioridad + 2*self.valor_tecnico)/4

    priorizacion = property(set_priorizacion)


class Nota(models.Model):
    """
        Clase para adjuntar una nota a un US
    """
    """Campos:"""
    nota = models.TextField()
    us = models.ForeignKey('UserStory', on_delete=models.CASCADE, null=True)
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.PROTECT, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nota


class Archivo(models.Model):
    """
        Clase para adjuntar un archivo a un US
    """
    """Campos:"""
    titulo = models.CharField(max_length=255, blank=True)
    archivo = models.FileField(upload_to='')
    fecha = models.DateTimeField(auto_now_add=True)
    us = models.ForeignKey('UserStory', on_delete=models.CASCADE, null=True)
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.titulo


class Actividad(models.Model):
    """
        Clase para agregar una actividad a un User Story
    """
    """Campos:"""
    nombre = models.CharField(max_length=20)
    descripcion = models.TextField()
    duracion = models.TimeField()
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.PROTECT, null=True)
    us = models.ForeignKey('UserStory', on_delete=models.CASCADE, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre