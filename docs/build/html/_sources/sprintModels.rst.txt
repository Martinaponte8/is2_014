Comentarios
============

from django.db import models
from django.core.exceptions import ValidationError
from proyecto.models import Proyecto
from django.utils import timezone
from datetime import timedelta
from userstory.models import UserStory

"""
Estados posibles del sprint
"""
PENDIENTE - EN PROCESO - TERMINADO (TO DO/DOING/DONE)
"""
ESTADOS_SPRINT = (
    ('Pendiente', 'Pendiente'),
    ('En Proceso', 'En Proceso'),
    ('Terminado', 'Terminado')
)

class Sprint(models.Model):
"""
    Modelo de la clase sprint, el cual representa un periodo de tiempo  definido dentro del
"""
proyecto al que se encuentra relacionado en el que se trabajan una cantidad definida de
""""
user stories
"""
    nombre = models.CharField(max_length=20, blank=False, null=False)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    proyecto = models.ForeignKey('proyecto.Proyecto',on_delete=models.CASCADE, null=True)
    estado = models.CharField(max_length=25, choices=ESTADOS_SPRINT, default='Pendiente')
    dias_laborales = models.IntegerField(null=False)
    dias_habiles = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
"""
     retorna el nombre del sprint
"""
        return self.nombre

    def has_dias_habiles(self):
"""
retorna falso si no se ha definido ningun dia habil en el sprint o verdadero en
"""
caso de que exista por lo menos un dia habil durante el sprint
"""
        if not self.dias_habiles:
            return False
        return True

    def get_dias_habiles(self):
"""
        retorna la lista de dias habiles definidos para el sprint, siendo
"""
        1: Lunes
"""
        2: Martes
"""
        3: Miercoles
"""
        4: Jueves
"""
        5: Viernes
"""
        6: Sábado
"""
        7: Domingo
"""
        dias_habiles = []
        dh = self.dias_habiles
        if dh:
            for d in dh.split(','):
                dias_habiles.append(int(d))
        return dias_habiles

    def get_nombres_dias_habiles(self):
"""
        retorna la lista nombres de dias habiles definidos para el sprint
"""
        1: Lunes
"""
        2: Martes
"""
        3: Miercoles
"""
        4: Jueves
"""
        5: Viernes
"""
        6: Sábado
"""
        7: Domingo
"""
        dias_habiles = []
        dh = self.dias_habiles
        if dh:
            for d in dh.split(','):
                if d == '1':
                    dias_habiles.append('Lunes')
                elif d == '2':
                    dias_habiles.append('Martes')
                elif d == '3':
                    dias_habiles.append('Miércoles')
                elif d == '4':
                    dias_habiles.append('Jueves')
                elif d == '5':
                    dias_habiles.append('Viernes')
                elif d == '6':
                    dias_habiles.append('Sábado')
                elif d == '7':
                    dias_habiles.append('Domingo')
        return dias_habiles

    def validate(self):
"""
        Metodo del modelo de Sprint que lanza excepciones de tipo ValidationError en caso de
"""
        que no se hayan completado todos los campos obligatorios en el sprint (dias hábiles,
"""
        nombre y días laborales) en caso contrario retorna verdadero
"""
        if not self.has_dias_habiles():
            raise ValidationError('Debe ingresar al menos un dia hábil')
        if not self.nombre:
            raise ValidationError('Debe ingresar el nombre del sprint')
        if not self.dias_laborales or self.dias_laborales == 0:
            raise ValidationError('Debe ingresar al menos un dia laboral')
        if not self.proyecto:
            raise ValidationError('En sprint debe estar relacionado a un proyecto')
        return True

    def validate_test(self):
"""
        Metodo del modelo de Sprint que retorna un booleano en caso
"""
        que no se hayan completado todos los campos obligatorios en el sprint.
"""
        if not self.has_dias_habiles():
            return False
        if not self.nombre:
            return False
        if not self.dias_laborales or self.dias_laborales == 0:
            return False
        if not self.proyecto:
            return False
        return True

    def get_duracion_real(self):
"""
        metodo del modelo Sprint que retorna la cantidad de dias de duracion del sprint en
"""
        días hábiles
"""
        :return:
"""
        :dias: la cantidad de dias entre la fecha de inicio del sprint y la fecha de finalizacion
"""
        del sprint, en caso de no tener fecha de finalizacion aun, hasta la fecha de hoy
"""
        if not self.fecha_inicio: return 0
        dias_habiles = self.get_dias_habiles()
        inicio = self.fecha_inicio
        if self.fecha_fin:
            fin = self.fecha_fin
        else:
            fin = timezone.now().date()
        currentdate = inicio
        dias = 0
        while currentdate <= fin:
            if currentdate.isoweekday() in dias_habiles:
                dias += 1
            currentdate += timedelta(days=1)
        return dias

    def get_user_stories(self):
"""
        metodo del modelo Sprint que retorna todos los user stories asignados al sprint
"""
        :return: Todos los user stories del sprint
"""
        return UserStory.objects.filter(sprint=self.pk)

    def get_horas_trabajadas(self):
"""
        metodo de la clase Sprint que retorna el total de horas trabajadas en el sprint
        :return: total de horas trabajadas en el sprint
"""
        actividades = Actividad.objects.filter(sprint=self.pk)
        horas = 0
        return horas

     def get_bdc_line(self):
"""
        metodo del modelo Sprint que retorna un JSON que representa la lista de coordenadas
        para el grafico de su correspondiente burn down chart y el total de horas trabajadas
        :return: lista de coordenadas para graficar el burn  down chart
"""
        if not self.fecha_inicio: return []
        while dia <= fin:
            if dia.isoweekday() in dias_habiles:
        return coordenadas


class Horas(models.Model):

"""
    Modelo de Horas, el cual es una relacion entre un team member perteneciente al proyecto al
"""
    que se relaciona el sprint en el que se están asignando las horas laborales
"""
    horas_laborales = models.IntegerField(blank=False, null=False)
    team_member = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE, null=True)
    sprint = models.ForeignKey('sprint.Sprint', on_delete=models.CASCADE, null=True)

    def validate(self):
"""
        Metodo del modelo de Horas que lanza excepciones de tipo ValidationError en caso de
"""
        que no se hayan completado dos los campos obligatorios en el sprint (horas laborales,
"""
        team member, sprint) en caso contrario retorna verdadero
"""
        if not self.horas_laborales or self.horas_laborales == 0:
            raise ValidationError("Debe especificar horas laborales por dia laboral para el team member")
        if not self.sprint:
            raise ValidationError("Las horas laborales deben estar relacionadas a un sprint")
        if not self.team_member:
            raise ValidationError("Debe especificar un team member")
        return True