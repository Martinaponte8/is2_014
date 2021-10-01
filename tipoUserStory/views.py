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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Tipos de User Stories"
        return context

    def get(self,request,*args,**kwargs):
        self.object = None
        self.object_list = TipoUserStory.objects.filter(proyecto=self.kwargs['pk_proyecto'])
        proyecto = Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])
        permisos = request.user.get_nombres_permisos(proyecto=self.kwargs['pk_proyecto'])
        return self.render_to_response(self.get_context_data(permisos=permisos, project=proyecto, object_list=self.object_list))

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

    def get(self, request, *args, **kwargs):
        self.object = None
        form = CreateUserStoryTypeForm()
        form.fields["proyecto"].initial = self.kwargs['pk_proyecto']
        flujos_all = Flujo.objects.filter(proyecto=self.kwargs['pk_proyecto'])
        f = form.fields['flujos'].widget
        flujos = []
        for flujo in flujos_all:
            flujos.append((flujo.id, flujo.nombre))
        f.choices = flujos
        permisos = request.user.get_nombres_permisos(proyecto=self.kwargs['pk_proyecto'])
        return self.render_to_response(self.get_context_data(permisos=permisos, form=form))


    def get_context_data(self, **kwargs):
        self.object = None
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear Tipo de User Story"
        context['project'] = Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])
        return context

    def post(self, request, *args, **kwargs):
        form = CreateUserStoryTypeForm(request.POST)
        flujos_all = Flujo.objects.filter(proyecto=self.kwargs['pk_proyecto'])
        f = form.fields['flujos'].widget
        flujos = []
        for flujo in flujos_all:
            flujos.append((flujo.id, flujo.nombre))
        f.choices = flujos
        if form.is_valid():
            form.save()
        else:
            return self.render_to_response(self.get_context_data(form=form))
        return HttpResponseRedirect('../')


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

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        initial = {
            'proyecto': self.object.proyecto.pk,
            'nombre': self.object.nombre,
            'descripcion': self.object.nombre,
            'flujos': self.object.flujos.all
        }
        form = UpdateUserStoryTypeForm(initial=initial)
        flujos_all = Flujo.objects.filter(proyecto=self.kwargs['pk_proyecto'])
        f = form.fields['flujos'].widget
        flujos = []
        for flujo in flujos_all:
            flujos.append((flujo.id, flujo.nombre))
        f.choices = flujos
        permisos = request.user.get_nombres_permisos(proyecto=self.kwargs['pk_proyecto'])
        return self.render_to_response(self.get_context_data(permisos=permisos, form=form))

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['title'] = "Modificar Tipo de User Story"
        context['project'] = Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])
        return context

    def get_object(self, queryset=None):
        return TipoUserStory.objects.get(pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        flujos_all = Flujo.objects.filter(proyecto=self.kwargs['pk_proyecto'])
        f = form.fields['flujos'].widget
        flujos = []
        for flujo in flujos_all:
            flujos.append((flujo.id, flujo.nombre))
        f.choices = flujos
        if form.is_valid():
            form.save()
        else:
            return self.render_to_response(self.get_context_data(form=form))
        return HttpResponseRedirect('../')

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
