from django.contrib import admin

# Register your models here.
from .models import *
from rol.models import Rol
from rol.models import Permiso

class ProyectoDetalleInLine(admin.TabularInline):
    model = ProyectoDetalle

class ProyectoAdmin(admin.ModelAdmin):
    inlines = (ProyectoDetalleInLine,)

admin.site.register(Proyecto,ProyectoAdmin)
