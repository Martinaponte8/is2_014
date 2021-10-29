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

    def get(self,request,*args,**kwargs):
        return self.render_to_response(self.get_context_data(permisos=permisos, project=proyecto,object_list=self.object_list))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UpdateFlujoView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

"""
Vista para la modificacion de flujo
"""
     def get(self,request,*args,**kwargs):
        return self.render_to_response(self.get_context_data(permisos=permisos,form=form, fases=fases_orden_formset))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        return Flujo.objects.get(pk=self.kwargs['pk'])

    def post(self,request,*args,**kwargs):
        if form.is_valid() and fases_formset.is_valid():
            return self.form_valid(form, fases_formset)
        else:
            return self.form_invalid(form, fases_formset)

    def form_valid(self, form, fases_formset):
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form,fases_formset):
        if fases_formset.vacio:
            fs_error = "El flujo debe tener al menos una fase"
        if fases_formset.sin_nombre:
            fs_error = "Las fases deben tener un nombre"
        return self.render_to_response(self.get_context_data(fs_error=fs_error, form=form, fases=fases_formset))

@method_decorator(login_required, name='dispatch')
class CreateFlujoView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """
    Vista de la creacion de Flujo
    """
    template_name = 'flujo/flujo.html'
    model = Flujo
    success_url = '../'
    form_class = CreateFlujoForm
    success_message = 'Se ha creado el flujo'

    def get_object(self, queryset=None):
        obj = Flujo()
        proyecto = Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])
        obj.proyecto = proyecto
        return obj

    def get(self,request,*args,**kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        fases_orden_formset = FaseFormSet()
        permisos = request.user.get_nombres_permisos(proyecto=self.kwargs['pk_proyecto'])
        return self.render_to_response(self.get_context_data(permisos=permisos, form=form, fases=fases_orden_formset))

    def get_context_data(self, **kwargs):
        context = super(CreateFlujoView,self).get_context_data(**kwargs)
        context['project'] = Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])
        context['title'] = "Crear Flujo"
        return context

    def post(self,request,*args,**kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        fases_formset = FaseFormSet(request.POST)
        if form.is_valid() and fases_formset.is_valid():
            return self.form_valid(form,fases_formset)
        else:
            return self.form_invalid(form,fases_formset)

    def form_valid(self, form, fases_formset):
        self.object = form.save()
        fases_formset.instance = self.object
        fases_formset.save()
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form,fases_formset):
        fs_error = None
        if fases_formset.vacio:
            fs_error = "El flujo debe tener al menos una fase"
        if fases_formset.sin_nombre:
            fs_error = "Las fases deben tener un nombre"
        return self.render_to_response(self.get_context_data(fs_error=fs_error, form=form, fases=fases_formset))

@method_decorator(login_required, name='dispatch')
class CreateFlujoView(SuccessMessageMixin, LoginRequiredMixin, CreateView):

"""
Vista de la creacion de Flujo
"""
    def get_object(self, queryset=None):
        obj = Flujo()
        return obj

    def get(self,request,*args,**kwargs):
        return self.render_to_response(self.get_context_data(permisos=permisos, form=form, fases=fases_orden_formset))

    def get_context_data(self, **kwargs):
        context = super(CreateFlujoView,self).get_context_data(**kwargs)
        return context

    def post(self,request,*args,**kwargs):
        if form.is_valid() and fases_formset.is_valid():
            return self.form_valid(form,fases_formset)
        else:
            return self.form_invalid(form,fases_formset)

    def form_valid(self, form, fases_formset):
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form,fases_formset):
        if fases_formset.vacio:
            fs_error = "El flujo debe tener al menos una fase"
        if fases_formset.sin_nombre:
            fs_error = "Las fases deben tener un nombre"
        return self.render_to_response(self.get_context_data(fs_error=fs_error, form=form, fases=fases_formset))


@method_decorator(login_required, name='dispatch')
class TableroTemplateView(LoginRequiredMixin, SuccessMessageMixin, TemplateView):

"""
Vista del tablero de los flujos
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
        return self.render_to_response(self.get_context_data(usuario=usuario, permisos=permisos))

    def get_context_data(self, **kwargs):
"""
Metodo que retorna un diccionario utilizado para pasar datos a las vistas
"""
:param kwargs: Diccionario de datos adicionales para el contexto
"""
:return: diccionario de contexto necesario para la correcta visualizacion de los datos
"""
        return context

    def post(self, request, *args, **kwargs):
"""
En este metodo se guardan los archivos, actividades o notas si lo que se agrega
"""
es un adjunto, o se mueve un US al estado siguiente o estado anterior o se mueve el
"""
US a una fase especifica si no paso el control de calidad o pasa a finalizado si es
"""
que paso el control de calidad, se toma una y solo una de las acciones mecionadas
"""
segun la consulta POST recibida
"""
:param request: consulta recibida
"""
:param args: argumentos adicionales
"""
:param kwargs: diccionario de datos adicionales
"""
:return: la respuesta a la consulta POST
"""
    return render(request,'flujo/tablero.html',self.get_context_data(s_fase=us.fase,usuario=usuario,
                                                                             modal=us.pk, permisos=permisos))
        elif 'siguiente' in request.POST.keys():
            return render(request,'flujo/tablero.html',self.get_context_data(s_fase=us.fase,usuario=usuario, permisos=permisos))

        if 'anterior' in request.POST.keys():
            return render(request, 'flujo/tablero.html',

        if 'finalizar' in request.POST.keys():
            #si se comenta este if y elif deja finalizar el sprint
            actividad = GuardarActividadForm(request.POST)

        return HttpResponseRedirect('./')


@method_decorator(login_required, name='dispatch')
class VerFlujoDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):

"""
Vista para ver un flujo, sin opciones de modificación
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
        return self.render_to_response(self.get_context_data(permisos=permisos))

    def get_context_data(self, **kwargs):
"""
Metodo que retorna un diccionario utilizado para pasar datos a las vistas
"""
:param kwargs: Diccionario de datos adicionales para el contexto
"""
:return: diccionario de contexto necesario para la correcta visualizacion de los datos
"""
        return context

    def get_object(self, queryset=None):
"""
Metodo que retorna el objeto a ser visualizado
"""
:param queryset:
"""
:return: El proyecto a ser modificado
"""
        return Flujo.objects.get(pk=self.kwargs['pk'])
