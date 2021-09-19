Comentarios
============

from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import TipoUserStory
from django.http import HttpResponseRedirect
from tipoUserStory.forms import CreateUserStoryTypeForm, UpdateUserStoryTypeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from proyecto.models import *
from flujo.models import *


@method_decorator(login_required, name='dispatch')
class tipoUserStoryListView(LoginRequiredMixin, ListView):

"""
    Vista de la lista de Tipos de User Story
"""
    template_name = 'tipoUserStory/list.html'
    model = TipoUserStory
    queryset = TipoUserStory.objects.all()


@method_decorator(login_required, name='dispatch')
class CreateUserStoryTypeView(SuccessMessageMixin, LoginRequiredMixin, CreateView):

"""
    Vista para la creacion de un Tipo de User Story
"""
    template_name = 'tipoUserStory/tipoUserStory.html'
    model = TipoUserStory
    success_url = '../'
    form_class = CreateUserStoryTypeForm
    success_message = 'Se ha creado el tipo de User Story'

    def get_object(self, queryset=None):
        obj = TipoUserStory()
        proyecto = Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])
        obj.proyecto = proyecto
        return obj

    d

    def get_context_data(self, **kwargs):
        self.object = None
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear Tipo de User Story"
        context['project'] = Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])
        return context



@method_decorator(login_required, name='dispatch')
class UpdateUserStoryTypeView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

"""
    Vista para la modificacion de un Tipo de User Story
"""
    template_name = 'tipoUserStory/tipoUserStory.html'
    model = TipoUserStory
    success_url = '../'
    form_class = UpdateUserStoryTypeForm
    success_message = 'Los cambios se guardaron correctamente'


    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['title'] = "Modificar Tipo de User Story"
        context['project'] = Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])
        return context

    def get_object(self, queryset=None):
        return TipoUserStory.objects.get(pk=self.kwargs['pk'])


"""
        Muestra el tipo de User Story
"""
@method_decorator(login_required, name='dispatch')
class VerUserStoryTypeDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = TipoUserStory
    template_name = 'tipoUserStory/ver_tipoUserStory.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Ver Tipo de User Story"
        return context

    def get_object(self, queryset=None):
        return TipoUserStory.objects.get(pk=self.kwargs['pk'])