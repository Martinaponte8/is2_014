
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from .models import Rol
from django.contrib.auth.models import User
from rol.forms import * 
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


def eliminar3(request, rol_id):
    rol = Rol.objects.get(id=rol_id)
    rol.delete()
    return redirect("index")

@method_decorator(login_required, name='dispatch')
class RolListView(LoginRequiredMixin, ListView):
    template_name = 'rol/list.html'
    model = Rol
    queryset = Rol.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Roles"
        return context


@method_decorator(login_required, name='dispatch')
class CreateRolView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'rol/rol.html'
    model = Rol
    success_url = '/index'
    form_class = CreateRolForm
    success_message = 'Se ha creado el rol'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Crear Rol"
        return context


@method_decorator(login_required, name='dispatch')

class UpdateRolView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'rol/rol.html'
    model = Rol
    # permission_required= 
    form_class = UpdateRolForm
    success_url = '/index'
    success_message = 'Los cambios se guardaron correctamente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Modificar Rol"
        return context

    def get_object(self, queryset=None):
        return Rol.objects.get(pk=self.kwargs['pk'])

    def get_absolute_url(self):
        return reverse('update_rol', kwargs={'pk': self.kwargs['pk']})
