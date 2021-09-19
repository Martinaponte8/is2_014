Comentarios
============

from django.views.generic import ListView, CreateView, UpdateView, TemplateView, DetailView
from django.http import HttpResponseRedirect
from .models import Sprint
from proyecto.models import Proyecto
from sprint.forms import CreateSprintForm, UpdateSprintForm
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from userstory.models import *
from django.contrib import messages

"""
Vista del Login
"""

@method_decorator(login_required, name='dispatch')
class SprintListView(LoginRequiredMixin, ListView):

"""
    Vista de la lista de Sprints
"""
    template_name = 'sprint/list.html'
    model = Sprint
    queryset = Sprint.objects.all()


@method_decorator(login_required, name='dispatch')
class CreateSprintView(SuccessMessageMixin, LoginRequiredMixin, CreateView):

"""
    Vista para la creacion de un Sprint
"""
    template_name = 'sprint/sprint.html'
    model = Sprint
    success_url = '../'
    form_class = CreateSprintForm
    success_message = 'Se ha creado el sprint'



@method_decorator(login_required, name='dispatch')
class UpdateSprintView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

"""
    Vista para la modificacion de un Sprint
"""
    template_name = 'sprint/sprint.html'
    model = Sprint
    form_class = UpdateSprintForm
    success_url = '/proyectos/ejecuciones/'
    success_message = 'Los cambios se guardaron correctamente'



@method_decorator(login_required, name='dispatch')
class AsignarUSUpdateView(LoginRequiredMixin, ListView):

"""
    Vista para la asignacion de user story
"""
    template_name = 'sprint/asignar_us.html'
    model = UserStory

    def get(self,request,*args,**kwargs):
        self.object = None
        self.object_list = UserStory.objects.filter(proyecto=self.kwargs['pk_proyecto'])
        proyecto = Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])
        sprint = Sprint.objects.get(pk=self.kwargs['sprint_pk'])
        return self.render_to_response(self.get_context_data(sprint=sprint,project=proyecto, object_list=self.object_list))


"""
    Vista para ver el sprint
"""
@method_decorator(login_required, name='dispatch')
class VerSprintDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = Sprint
    template_name = 'sprint/ver_sprint.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Ver Sprint"
        return context

    def get_object(self, queryset=None):
        return Sprint.objects.get(pk=self.kwargs['pk'])