Comentarios
============

ffrom django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.http import HttpResponseRedirect
from .forms import *
from proyecto.models import *
from sprint.forms import CreateSprintForm, UpdateSprintForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from userstory.models import *
from flujo.models import *
from django.forms import inlineformset_factory
from django.db import transaction
import json
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.http import HttpResponseRedirect

from is2_014 import settings
from .forms import *
from proyecto.models import *
from sprint.forms import CreateSprintForm, UpdateSprintForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from userstory.models import *
from flujo.models import *
from django.forms import inlineformset_factory
from django.db import transaction
import json
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from io import BytesIO
from reportlab.pdfgen import canvas
import locale
from django.views.generic import View
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, TA_CENTER, TA_LEFT
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Line
from reportlab.lib.enums import TA_RIGHT
from reportlab.platypus import (
        Paragraph,
        Table,
        SimpleDocTemplate,
        Spacer,
        TableStyle,
        Paragraph,
        Image)

"""
Vista del Login
"""

@method_decorator(login_required, name='dispatch')
class SprintListView(LoginRequiredMixin, ListView):
"""
Vista de la lista de todos los Sprints del proyecto
"""

    queryset = Sprint.objects.all()

    def get_context_data(self, **kwargs):
"""
Metodo que retorna un diccionario utilizado para pasar datos a las vistas
"""
:param kwargs: Diccionario de datos adicionales para el contexto
"""
:return: diccionario de contexto necesario para la correcta visualizacion de los datos
"""
        context = super().get_context_data(**kwargs)
        try:
            context['sprint_pendiente'] = Sprint.objects.get(proyecto=self.kwargs['pk_proyecto'],estado='Pendiente')
        except:
            pass
        context['direccion'] = {}
        return context

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
        self.object = None
        return self.render_to_response(self.get_context_data(project=proyecto, object_list=self.object_list,permisos=permisos))


@method_decorator(login_required, name='dispatch')
class CreateSprintView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
"""
Vista para la creacion de un Sprint
"""
    def get_object(self, queryset=None):
"""
Metodo que retorna el objeto a ser creado con el proyecto actual asignado
"""
:param queryset:
"""
:return: el objeto actual con el proyecto seleccionado pre-asignado
"""
        obj = Sprint()
        return obj

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
        return self.render_to_response(self.get_context_data(team=team, horas_formset=horas_team, form=form,
                                                             permisos=permisos, formularios=formularios))

    def post(self, request, *args, **kwargs):
"""
Metodo que es ejecutado al darse una consulta POST
"""
:param request: consulta recibida
"""
:param args: argumentos adicionales
"""
:param kwargs: diccionario de datos adicionales
"""
:return: la respuesta a la consulta POST
"""
        if form.is_valid() and horas_team.is_valid():
            try:
                return self.render_to_response(self.get_context_data(team=team, horas_formset=horas_team,
                                                                     permisos=permisos, formularios=formularios,
                                                                     form_error=form_error))
        else:
            return self.render_to_response(self.get_context_data(team=team, horas_formset=horas_team,
                                                                 permisos=permisos, formularios=formularios))

    def get_context_data(self, **kwargs):
"""
Metodo que retorna un diccionario utilizado para pasar datos a las vistas
"""
:param kwargs: Diccionario de datos adicionales para el contexto
"""
:return: diccionario de contexto necesario para la correcta visualizacion de los datos
"""
        self.object = None
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class UpdateSprintView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
"""
Vista para la modificacion de un Sprint
"""
    def get(self, request, *args, **kwargs):
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
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data(permisos=permisos))

    def get_context_data(self, **kwargs):
"""
Metodo que retorna un diccionario utilizado para pasar datos a las vistas
"""
:param kwargs: Diccionario de datos adicionales para el contexto
"""
:return: diccionario de contexto necesario para la correcta visualizacion de los datos
"""
        context = super().get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
"""
Metodo que retorna el objeto a ser modificado
"""
:param queryset:
"""
:return: el objeto actual
"""
        return Sprint.objects.get(pk=self.kwargs['sprint_pk'])

    def post(self, request, *args, **kwargs):
"""
Metodo que es ejecutado al darse una consulta POST
"""
:param request: consulta recibida
"""
:param args: argumentos adicionales
"""
:param kwargs: diccionario de datos adicionales
"""
:return: la respuesta a la consulta POST
"""
            return HttpResponseRedirect('./')
        #fin reasignacion de team members
        if form.is_valid() and horas_team.is_valid():
            try:
                    return HttpResponseRedirect(self.success_url)
            except ValidationError as e:
                return self.render_to_response(self.get_context_data(team=team, horas_formset=horas_team,
                                                                     permisos=permisos, formularios=formularios,
                                                                     form_error=form_error))
        else:
            formularios = {}
            for ht in horas_team:
            return self.render_to_response(self.get_context_data(team=team, horas_formset=horas_team,
                                                                 permisos=permisos, formularios=formularios))


@method_decorator(login_required, name='dispatch')
class AsignarUSUpdateView(LoginRequiredMixin, ListView):
"""
Vista para la asignacion de user story
"""
    def get_queryset(self):
"""
retorna la lista de todos los user stories pendientes actualmente
"""
        pendientes = UserStory.objects.filter(proyecto=self.kwargs['pk_proyecto'],
                                                estado=2)
        return asignados.union(pendientes)

    def get_pendientes_clasificados(self,sprint):
        """retorna dos listas, primero una lista de todos los user stories pendientes
        que ya han sido trabajados en otro sprint ordenados por priorizacion y segundo
        la lista de todos los user stories pendientes que aun no han sido trabajados
        ordenados por priorizacion"""
        sl = []
        fl = []
        return fl, sl

    def get(self,request,*args,**kwargs):
        """retorna el contexto y permisos de usuario que constituyen la respuesta a las
        consultas GET
        Metodo que es ejecutado al darse una consulta GET
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta GET
        """
        self.object_list = self.get_queryset()
        permisos = request.user.get_nombres_permisos(proyecto=self.kwargs['pk_proyecto'])
        return self.render_to_response(self.get_context_data(permisos=permisos))

    def get_context_data(self, *, object_list=None, **kwargs):
"""
Metodo que retorna un diccionario utilizado para pasar datos a las vistas
"""
:param kwargs: Diccionario de datos adicionales para el contexto
"""
:return: diccionario de contexto necesario para la correcta visualizacion de los datos
"""
        context = super(AsignarUSUpdateView,self).get_context_data(**kwargs)
        return context

    def post(self,request,*args,**kwargs):
"""
Metodo que valida las asignaciones realizadas por el usuario, de ser validas guarda el user
"""
story asignado al sprint pendiente, de no ser validas regresa a la vista de asignacion
"""
para visualizar los errores
"""
:param request: consulta recibida
"""
:param args: argumentos adicionales
"""
:param kwargs: diccionario de datos adicionales
"""
:return: la respuesta a la consulta POST
"""
        self.object_list = self.get_queryset()
            if str(us.pk) in asigned:
                '''Se asignan los us al sprint'''
                    return self.render_to_response(self.get_context_data(permisos=permisos,
                                                                         error_msg=error_msg,
                                                                         set_team_members=True))
            else:
                '''Se quita la asignacion a todos los us que no fueron seleccionados'''
                us.save()
        return HttpResponseRedirect('../../../')

@method_decorator(login_required, name='dispatch')
class VerSprintDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
"""
Clase de la vista utilizada para visualizar los sprints sin opciones de modificacion
"""
    def get(self, request, *args, **kwargs):
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
        permisos = request.user.get_nombres_permisos(proyecto=self.kwargs['pk_proyecto'])
        return self.render_to_response(self.get_context_data(permisos=permisos))

    def get_context_data(self, **kwargs):
"""
Metodo que retorna un diccionario utilizado para pasar datos a las vistas
"""
:param kwargs: Diccionario de datos adicionales para el contexto
"""
:return: diccionario de contexto necesario para la correcta visualizacion de los datos
"""
        context = super().get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
"""
Metodo que retorna el objeto actual
"""
:param queryset:
"""
:return: el objeto actual
"""
        return sprint

@method_decorator(login_required, name='dispatch')
class SprintBacklogPDF(View):
    """
    Clase de la vista para creacion de Reporte Sprint Backlog
    """
    def get(self, request, *args, **kwargs):
"""
        respuesta a la consulta GET
        :param request: consulta GET
        :param args: argumentos
        :param kwargs: diccionario de datos
        :return: respuesta a consultas GET
"""
        se crea el pdf
"""
        self.encabezado()
        self.titulo()
        self.descripcion()
        self.crearTabla()

        buffer.close()
        response.write(pdf)
        return response

    def encabezado(self):
"""
        agrega el encabezado al documento pdf a imprimir :return: None
"""
        self.story.append(tabla)
        d.add(Line(0, 0, 480, 0))
        self.story.append(d)
        self.story.append(Spacer(1, 0.3 * inch))

    def titulo(self):
"""
        agrega el titulo al documento pdf a imprimir
        :return: None
"""
        self.story.append(p)
        self.story.append(Spacer(1, 0.5 * inch))

    def descripcion(self):
"""
        agrega la descripcion al documento pdf
        :return: None
"""
        self.story.append(p)
        self.story.append(Spacer(1, 0.3 * inch))

    def crearTabla(self):
"""
        agrega el cuerpo del reporte al documento pdf
        :return: None
"""
        for us in user_stories:
            for actividad in actividades:
            us.horas_trabajadas = horas
        for x in user_stories:
            data.append(aux)
        style = TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')])
        t.setStyle(style)
        self.story.append(t)

    def estiloPC(self):
"""
        estilo del cuerpo del reporte
        :return: objeto para estilo del reporte
"""
        return ParagraphStyle(name="centrado", alignment=TA_CENTER)

    def estiloPL(self):
"""
        estilo de la descripcion del reporte :return: objeto para estilo del reporte
"""
        return ParagraphStyle(name="izquierda", alignment=TA_LEFT)

    def estiloPR(self):
"""
        estilo el encabezado del reporte :return: objeto para estilo del reporte
"""
        return ParagraphStyle(name="derecha", alignment=TA_RIGHT)

    def numeroPagina(self, canvas, doc):
"""
        agrega el numero de pagina al documento pdf
        :param canvas: pdf
        :param doc: documento pdf
        :return: None
"""
        canvas.drawRightString(190 * mm, 20 * mm, text)

@method_decorator(login_required, name='dispatch')
class PrioridadesPDF(View):
"""
    clase de la vista para creacion de Reporte de Prioridades de sprint
"""
    def get(self, request, *args, **kwargs):
"""
        respuesta a la consulta GET
        :param request: consulta GET
        :param args: argumentos
        :param kwargs: diccionario de datos
        :return: respuesta a consultas GET
"""
        self.encabezado()
        self.titulo()
        self.descripcion()
        self.crearTabla()
        buffer.close()
        response.write(pdf)
        return response

    def encabezado(self):
"""
        agrega el encabezado al documento pdf
        :return: None
"""
        self.story.append(tabla)
        d.add(Line(0, 0, 480, 0))
        self.story.append(d)
        self.story.append(Spacer(1, 0.3 * inch))

    def titulo(self):
"""
        agrega el titulo al documento pdf :return: None
"""
        self.story.append(p)
        self.story.append(Spacer(1, 0.5 * inch))

    def descripcion(self):
"""
        agrega la descripcion al documento pdf :return: None
"""
        self.story.append(p)
        self.story.append(Spacer(1, 0.3 * inch))

    def crearTabla(self):
"""
        agrega el cuerpo del reporte pdf :return: None
"""
        for us in us_query:
            if us.estado != 0 and us.sprints_asignados.count() >= 2:
                l1.append(us)
            elif (us.estado == 1 or us.estado == 0):
                l2.append(us)
            else:
                l3.append(us)
        l1.sort(key=lambda x: x.priorizacion, reverse=True)
        l2.sort(key=lambda x: x.priorizacion, reverse=True)
        l3.sort(key=lambda x: x.priorizacion, reverse=True)
        for us in l1:
            user_stories.append(us)
        for us in l2:
            user_stories.append(us)
        for us in l3:
            user_stories.append(us)
        for x in user_stories:
            data.append(aux)
        style = TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')])

        t.setStyle(style)
        self.story.append(t)

    def estiloPC(self):
"""
        :return: estilo para cuerpo del reporte
"""
        return ParagraphStyle(name="centrado", alignment=TA_CENTER)

    def estiloPL(self):
"""
        :return: estilo para descripcion del reporte
"""
        return ParagraphStyle(name="izquierda", alignment=TA_LEFT)

    def estiloPR(self):
"""
        :return: estilo para encabezado del reporte
"""
        return ParagraphStyle(name="derecha", alignment=TA_RIGHT)

    def numeroPagina(self, canvas, doc):
"""
        agrega el numero de pagina al documento pdf
        :param canvas: pdf
        :param doc: documento pdf
        :return: None
"""
        canvas.drawRightString(190 * mm, 20 * mm, text)