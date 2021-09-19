Comentarios
============


from django.views.generic import ListView, CreateView, UpdateView, TemplateView, DetailView
from .forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from proyecto.models import *
from sprint.models import *
from userstory.models import *
from userstory.forms import *


@method_decorator(login_required, name='dispatch')
class FlujoListView(LoginRequiredMixin, ListView):

"""
Vista de la lista de Flujos
"""
    template_name = 'flujo/list.html'
    model = Flujo
    queryset = Flujo.objects.all()

class UpdateFlujoView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

"""
Vista para la modificacion de flujo
"""
    template_name = 'flujo/flujo.html'
    model = Flujo
    success_url = '../'
    form_class = UpdateFlujoForm
    success_message = 'Se ha modificado el flujo'

class CreateFlujoView(SuccessMessageMixin, LoginRequiredMixin, CreateView):

"""
Vista de la creacion de Flujo
"""
    template_name = 'flujo/flujo.html'
    model = Flujo
    success_url = '../'
    form_class = CreateFlujoForm
    success_message = 'Se ha creado el flujo'

class TableroTemplateView(LoginRequiredMixin, SuccessMessageMixin, TemplateView):

"""
Vista del tablero de los flujos
"""
    template_name = 'flujo/tablero.html'

def post(self, request, *args, **kwargs):

"""
En este metodo se guardan los archivos, actividades o notas si lo que se agrega es un adjunto, o se mueve un US
"""
al estado siguiente o estado anterior o se mueve el US a una fase especifica si no paso el control de calidad o pasa
"""
a finalizado si es que paso el control de calidad, se toma una y solo una de las acciones mecionadas segun la consulta POST recibida
"""


