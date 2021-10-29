Comentarios
============

from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import UserStory
from userstory.forms import CreateUserStoryForm, UpdateUserStoryForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from tipoUserStory.models import *
from userstory.models import *


"""
Funcion eliminar UserStory
"""
def eliminar4(request,pk_proyecto,us_id):
    return redirect("index")

@method_decorator(login_required, name='dispatch')
class UserStoryListView(LoginRequiredMixin, ListView):
"""
Vista de la lista de UserStory
"""

    def get(self,request,*args,**kwargs):
"""
Metodo que es ejecutado al darse una consulta GET
"""
:param request: consulta recibida
"""
:param args: argumentos adicionales
"""
:param kwargs: diccionario de datos adicionales
"""
:return: la respuesta a la consulta GET
"""
        return self.render_to_response(self.get_context_data(project=proyecto,object_list=self.object_list,permisos=permisos))

    def get_context_data(self, **kwargs):
"""
Metodo que retorna un diccionario utilizado para pasar datos a las vistas
"""
:param kwargs: Diccionario de datos adicionales para el contexto
"""
:return: diccionario de contexto necesario para la correcta visualizacion de los datos
"""
        context = super(UserStoryListView,self).get_context_data(**kwargs)
        context['title'] = 'Usuarios'
        context['direccion'] = {}
        context['direccion']['Usuarios'] = (1, '/usuarios/')
        return context


@method_decorator(login_required, name='dispatch')
class CreateUserView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
"""
    Vista para la creacion de un Usuario
"""

    def get(self, request, *args, **kwargs):
"""
        Metodo que es ejecutado al darse una consulta GET
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta GET
"""
        return self.render_to_response(self.get_context_data(permisos=permisos))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear Usuario"
        context['direccion'] = {}
        context['direccion']['Usuarios'] = (1, '/usuarios/')
        context['direccion']['Crear Usuario'] = (2, '/usuarios/create/')
        return context

    def post(self, request, *args, **kwargs):
"""
        Metodo que es ejecutado al darse una consulta POST
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta POST
"""
        if form.is_valid():
            return HttpResponseRedirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(permisos=permisos, form=form))


@method_decorator(login_required, name='dispatch')
class UpdateUserView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
"""
    Vista para la modificacion de un Usuario
"""

    def get(self, request, *args, **kwargs):
"""
        Metodo que es ejecutado al darse una consulta GET
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta GET
"""
        return self.render_to_response(self.get_context_data(permisos=permisos))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modificar Usuario"+ str(self.object.pk)
        context['direccion'] = {}
        context['direccion']['Usuarios'] = (1, '/usuarios/')
        context['direccion']['Modificar: ' + self.object.username] = (2, '/usuarios/modificar/' + str(self.object.pk) + '/')
        return context

    def get_object(self, queryset=None):
        return Usuario.objects.get(pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
"""
        Metodo que es ejecutado al darse una consulta POST
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta POST
"""
        if form.is_valid():
            self.object = form.save()
            return HttpResponseRedirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(permisos=permisos, form=form))

    def get_absolute_url(self):
        return reverse('update_user', kwargs={'pk': self.kwargs['pk']})


@method_decorator(login_required, name='dispatch')
class VerUserDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
"""
    Vista de los detalles de un Usuario
"""
    model = Usuario
    template_name = 'usuarios/ver_user.html'

    def get(self, request, *args, **kwargs):
"""
        Metodo que es ejecutado al darse una consulta GET
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta GET
"""
        return self.render_to_response(self.get_context_data(permisos=permisos))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Ver Usuario" + str(self.object.pk)
        context['direccion'] = {}
        context['direccion']['Usuarios'] = (1, '/usuarios/')
        context['direccion']['Ver: ' + self.object.username] = (2, '/usuarios/ver/' + str(self.object.pk) + '/')
        return context

    def get_object(self, queryset=None):
        return Usuario.objects.get(pk=self.kwargs['pk'])

