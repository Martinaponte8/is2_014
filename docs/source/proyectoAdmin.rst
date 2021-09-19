Comentarios
============

from django.contrib import admin

# Register your models here.
from .models import *
from rol.models import Rol
from rol.models import Permiso


class TeamMemberInLine(admin.TabularInline):
    model = TeamMember

class ProyectoAdmin(admin.ModelAdmin):
    inlines = (TeamMemberInLine,)


admin.site.register(Proyecto,ProyectoAdmin)

