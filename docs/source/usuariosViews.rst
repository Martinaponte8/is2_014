Comentarios
============

from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

"""
Funcion eliminar Usuario
"""
def eliminar(request, user_id):
    user = Usuario.objects.get(id=user_id)
    user.delete()
    return redirect("index")



@method_decorator(login_required, name='dispatch')
class UserListView(LoginRequiredMixin, ListView):
"""
    Vista de la lista de Usuarios
"""
    template_name = 'usuarios/list.html'
    model = Usuario
    queryset = Usuario.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Usuarios"
        return context


@method_decorator(login_required, name='dispatch')
class CreateUserView(SuccessMessageMixin, LoginRequiredMixin, CreateView):

"""
    Vista para la creacion de un Usuario
"""
    template_name = 'usuarios/user.html'
    model = Usuario
    success_url = '/usuarios/'
    form_class = CreateUserForm
    success_message = 'Se ha creado el usuario'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear Usuario"
        return context


@method_decorator(login_required, name='dispatch')
class UpdateUserView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

"""
    Vista para la modificacion de un Usuario
"""
    template_name = 'usuarios/user.html'
    model = Usuario
    form_class = UpdateUserForm
    success_url = '/usuarios/'
    success_message = 'Los cambios se guardaron correctamente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modificar Usuario"
        return context

    def get_object(self, queryset=None):
        return Usuario.objects.get(pk=self.kwargs['pk'])

    def get_absolute_url(self):
        return reverse('update_user', kwargs={'pk': self.kwargs['pk']})


@method_decorator(login_required, name='dispatch')
class VerUserDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):

"""
    Vista de los detalles de un Usuario
"""
    model = Usuario
    template_name = 'usuarios/ver_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Ver Usuario"
        return context

    def get_object(self, queryset=None):
        return Usuario.objects.get(pk=self.kwargs['pk'])
