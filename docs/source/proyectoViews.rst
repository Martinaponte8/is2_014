Comentarios
============

from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .forms import *
from proyecto.forms import CreateProjectForm, UpdateProjectForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from sprint.models import *
from flujo.models import *
from django.utils import timezone
from userstory.models import *

from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from .models import *
from .forms import *
from proyecto.forms import CreateProjectForm, UpdateProjectForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden,HttpResponseRedirect
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from sprint.models import *
from flujo.models import *
from django.utils import timezone
from userstory.models import *
from .models import Proyecto

"""
Vistas del Proyecto
"""

"""
Funcion eliminar Proyecto
"""

def eliminar2(request, project_id):
    project = Proyecto.objects.get(id=project_id)
    project.delete()
    return redirect("index")

class ProjectListView(LoginRequiredMixin, ListView):

"""
Vista de la lista de Proyectos
"""
    template_name = 'proyecto/list.html'
    model = Proyecto
    queryset = Proyecto.objects.all()

class CreateProjectView(SuccessMessageMixin, LoginRequiredMixin, CreateView):

"""
    Vista de la creacion de un nuevo Proyecto
"""
    template_name = 'proyecto/proyecto.html'
    model = Proyecto
    success_url = '/proyectos/'
    form_class = CreateProjectForm
    success_message = 'Se ha creado el proyecto'

class UpdateProjectView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

"""
    Vista de la modificacion de un Proyecto
"""
    template_name = 'proyecto/proyecto.html'
    model = Proyecto
    form_class = UpdateProjectForm
    success_url = '/proyectos/'
    success_message = 'Los cambios se guardaron correctamente'


"""
Vistas de Opciones de Proyecto
"""

@method_decorator(login_required, name='dispatch')
class OptionsListView(LoginRequiredMixin, ListView):

"""
    Vista de la lista de opciones para administrar un proyecto existente
"""
    template_name = 'proyecto/opciones_list.html'
    model = Proyecto
    queryset = Proyecto.objects.all()

"""
Actualizar la opciones de vista
"""
@method_decorator(login_required, name='dispatch')
class UpdateOptionsView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

"""
Vistas para modificacion de las opciones de proyecto
"""
    template_name = 'proyecto/options.html'
    model = Proyecto
    form_class = UpdateProjectForm
    success_url = '/proyectos/opciones/'
    success_message = 'Los cambios se guardaron correctamente'

"""
Vistas de Ejecucion
"""


@method_decorator(login_required, name='dispatch')
class EjecucionListView(LoginRequiredMixin, ListView):

"""
    Vista de la lista de los proyectos en ejecucion
"""
    template_name = 'proyecto/ejecuciones_list.html'
    model = Proyecto
    queryset = Proyecto.objects.all()

"""
Actualiza la vista de ejecucion
"""
@method_decorator(login_required, name='dispatch')
class UpdateEjecucionView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

"""
    Vista de las modificaciones de los proyectos en ejecucion
"""
    template_name = 'proyecto/ejecucion.html'
    model = Proyecto
    form_class = UpdateProjectForm
    success_url = '/proyectos/ejecuciones/'
    success_message = 'Los cambios se guardaron correctamente'

"""
    Cambiar el estado de un proyecto
"""
    Opciones = Iniciar - Terminar -Suspender - Cancelar - Reiniciar
"""
    def post(self, request, *args, **kwargs):
        #se debe iniciar el proyecto
        proyecto = self.get_object()

"""
Actualiza el team Member
"""

@method_decorator(login_required, name='dispatch')
class UpdateTeamMemberView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
"""
    Vista de la modificacion del TeamMember
"""
    template_name = 'proyecto/asignacion_roles.html'
    model = Proyecto
    form_class = UpdateProjectForm
    success_url = '../'
    success_message = 'Los cambios se guardaron correctamente'

