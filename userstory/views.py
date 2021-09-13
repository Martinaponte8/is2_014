from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import UserStory
from userstory.forms import CreateUserStoryForm, UpdateUserStoryForm
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from tipoUserStory.models import *


@method_decorator(login_required, name='dispatch')
class UserStoryListView(LoginRequiredMixin, ListView):
    """
    Vista de la lista de UserStory
    """
    template_name = 'userstory/list.html'
    model = UserStory
    queryset = UserStory.objects.all()

    def get(self,request,*args,**kwargs):
        self.object = None
        self.object_list = UserStory.objects.filter(proyecto=self.kwargs['pk_proyecto'])
        proyecto = Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])
        permisos = request.user.get_nombres_permisos(proyecto=self.kwargs['pk_proyecto'])
        return self.render_to_response(self.get_context_data(project=proyecto,object_list=self.object_list,permisos=permisos))


@method_decorator(login_required, name='dispatch')
class CreateUserStoryView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """
    Vista para la creacion de un User Story
    """
    template_name = 'userstory/userstory.html'
    model = UserStory
    success_url = '../'
    form_class = CreateUserStoryForm
    success_message = 'Se ha creado el user story'

    def get_object(self, queryset=None):
        obj = UserStory()
        proyecto = Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])
        obj.proyecto = proyecto
        return obj

    def get(self,request,*args,**kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])
        context['tipos_us'] = TipoUserStory.objects.filter(proyecto=self.kwargs['pk_proyecto'])
        context['flujos'] = {}
        for tipo in context['tipos_us']:
            if tipo.pk not in context['flujos'].keys():
                context['flujos'][tipo.pk] = tipo.flujos.all
        context['title'] = "Crear User Story"
        return context


@method_decorator(login_required, name='dispatch')
class UpdateUserStoryView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Vista para la modificacion de un User Story
    """
    template_name = 'userstory/userstory.html'
    model = UserStory
    form_class = UpdateUserStoryForm
    success_url = '../'
    success_message = 'Los cambios se guardaron correctamente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])
        context['tipos_us'] = TipoUserStory.objects.filter(proyecto=self.kwargs['pk_proyecto'])
        context['flujos'] = {}
        for tipo in context['tipos_us']:
            if tipo.pk not in context['flujos'].keys():
                context['flujos'][tipo.pk] = tipo.flujos.all
        context['title'] = "Modificar User Story"
        return context

    def get_object(self, queryset=None):
        return UserStory.objects.get(pk=self.kwargs['pk'])

    def get_absolute_url(self):
        return reverse('update_userstory', kwargs={'pk': self.kwargs['pk']})


@method_decorator(login_required, name='dispatch')
class VerUserStoryDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = UserStory
    template_name = 'userstory/ver_userstory.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Ver UserStory"
        return context

    def get_object(self, queryset=None):
        return UserStory.objects.get(pk=self.kwargs['pk'])


@method_decorator(login_required, name='dispatch')
class ProductBacklogListView(LoginRequiredMixin, ListView):
    """
    Vista del Product Backlog
    """
    template_name = 'userstory/ProductBacklog.html'
    model = UserStory

    def get(self,request,*args,**kwargs):
        self.object = None
        self.object_list = UserStory.objects.filter(proyecto=self.kwargs['pk_proyecto'])
        ol = []
        for us in self.object_list:
            ol.append(us)
        ol.sort(key=lambda x: x.priorizacion, reverse=True)
        proyecto = Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])
        return self.render_to_response(self.get_context_data(project=proyecto, ol=ol))


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductBacklogListView,self).get_context_data(**kwargs)
        context['title'] = "Product Backlog"
        return context
