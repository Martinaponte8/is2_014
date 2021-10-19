from django.contrib import admin
from .models import *

admin.site.register(UserStory)
admin.site.register(Nota)
admin.site.register(Archivo)
admin.site.register(Actividad)
admin.site.register(HistorialEstimaciones)
admin.site.register(CambioEstado)

