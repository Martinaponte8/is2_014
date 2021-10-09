from django.views.generic import ListView, CreateView, UpdateView, DetailView
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
# from django.core.mail import EmailMessage
# from io import BytesIO
# from reportlab.pdfgen import canvas
# import locale
# from django.views.generic import View
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.styles import ParagraphStyle, TA_CENTER, TA_LEFT
# from reportlab.lib.units import inch, mm
# from reportlab.lib import colors
# from reportlab.graphics.shapes import Drawing, Line
# from reportlab.lib.enums import TA_RIGHT
# from reportlab.platypus import (
#         Paragraph,
#         Table,
#         SimpleDocTemplate,
#         Spacer,
#         TableStyle,
#         Paragraph,
#         Image)


"""
Vista del Login
"""

@method_decorator(login_required, name='dispatch')
class SprintListView(LoginRequiredMixin, ListView):
    """
    Vista de la lista de todos los Sprints del proyecto
    """
    template_name = 'sprint/list.html'
    model = Sprint
    queryset = Sprint.objects.all()

    def get_context_data(self, **kwargs):
        """
        Metodo que retorna un diccionario utilizado para pasar datos a las vistas
        :param kwargs: Diccionario de datos adicionales para el contexto
        :return: diccionario de contexto necesario para la correcta visualizacion de los datos
        """
        context = super().get_context_data(**kwargs)
        context['title'] = "Sprints de Proyecto"
        try:
            context['sprint_pendiente'] = Sprint.objects.get(proyecto=self.kwargs['pk_proyecto'],estado='Pendiente')
        except:
            pass
        context['direccion'] = {}
        context['direccion']['Ejecuciones'] = (1, '/proyectos/ejecuciones/')
        proyecto = Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])
        context['direccion'][proyecto.nombre] = (1, '/proyectos/ejecuciones/' + str(proyecto.pk) + '/')
        context['direccion']['Sprints'] = (1, '/proyectos/ejecuciones/' + str(proyecto.pk) + '/sprints/')
        return context

    def get(self,request,*args,**kwargs):
        """
        Metodo que es ejecutado al darse una consulta GET
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta GET
        """
        self.object = None
        self.object_list = Sprint.objects.filter(proyecto=self.kwargs['pk_proyecto']).order_by('-pk')
        permisos = request.user.get_nombres_permisos(proyecto=self.kwargs['pk_proyecto'])
        proyecto = Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])
        return self.render_to_response(self.get_context_data(project=proyecto, object_list=self.object_list,permisos=permisos))


@method_decorator(login_required, name='dispatch')
class CreateSprintView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """
    Vista para la creacion de un Sprint
    """
    template_name = 'sprint/sprint.html'
    model = Sprint
    success_url = '../../'
    form_class = CreateSprintForm
    success_message = 'Se ha creado el sprint'

    def get_object(self, queryset=None):
        """
        Metodo que retorna el objeto a ser creado con el proyecto actual asignado
        :param queryset:
        :return: el objeto actual con el proyecto seleccionado pre-asignado
        """
        obj = Sprint()
        proyecto = Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])
        obj.proyecto = proyecto
        return obj

    def get(self,request,*args,**kwargs):
        """
        Metodo que es ejecutado al darse una consulta GET
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta GET
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        permisos = request.user.get_nombres_permisos(proyecto=self.kwargs['pk_proyecto'])
        team = TeamMember.objects.filter(proyecto=self.kwargs['pk_proyecto'])
        DiasLaboralesFormSet = inlineformset_factory(Sprint, Horas, form=HorasForm, extra=len(team))
        horas_team = DiasLaboralesFormSet()
        form_nr = 0
        formularios = {}
        for tm in team:
            f = horas_team[form_nr]
            f.fields['team_member'].initial = tm.usuario.pk
            if tm.usuario.pk not in formularios.keys():
                formularios[tm.usuario.pk] = {}
            formularios[tm.usuario.pk]['usuario'] = tm.usuario.username
            formularios[tm.usuario.pk]['formulario'] = f
            form_nr += 1
        return self.render_to_response(self.get_context_data(team=team, horas_formset=horas_team, form=form,
                                                             permisos=permisos, formularios=formularios))

    def post(self, request, *args, **kwargs):
        """
        Metodo que es ejecutado al darse una consulta POST
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta POST
        """
        dias_habiles = str(request.POST.getlist('dias_habiles'))[1:-1].replace("'", "")
        dias_habiles = dias_habiles.replace(" ", "")
        permisos = request.user.get_nombres_permisos(proyecto=self.kwargs['pk_proyecto'])
        self.object = self.get_object()
        formclass = self.get_form_class()
        form = self.get_form(formclass)
        team = TeamMember.objects.filter(proyecto=self.kwargs['pk_proyecto'])
        horas_team = HorasFormSet(request.POST)
        if form.is_valid() and horas_team.is_valid():
            try:
                with transaction.atomic():
                    self.object = form.save()
                    self.object.validate()
                    horas_team.instance = self.object
                    Horas.objects.filter(sprint=self.object).delete()
                    horas_team.save()
                    return HttpResponseRedirect(self.success_url)
            except ValidationError as e:
                form_error = e.message
                formularios = {}
                from usuarios.models import Usuario
                for ht in horas_team:
                    usuario = Usuario.objects.get(pk=ht['team_member'].value())
                    if usuario.pk not in formularios.keys():
                        formularios[usuario.pk] = {}
                    formularios[usuario.pk]['usuario'] = usuario.username
                    formularios[usuario.pk]['formulario'] = ht
                return self.render_to_response(self.get_context_data(team=team, horas_formset=horas_team,
                                                                     permisos=permisos, formularios=formularios,
                                                                     form_error=form_error))
        else:
            formularios = {}
            from usuarios.models import Usuario
            for ht in horas_team:
                usuario = Usuario.objects.get(pk=ht.cleaned_data['team_member'])
                if usuario.pk not in formularios.keys():
                    formularios[usuario.pk] = {}
                usuario = Usuario.objects.get(pk=ht.cleaned_data[''])
                formularios[usuario.pk]['usuario'] = usuario.username
                formularios[usuario.pk]['formulario'] = ht
            return self.render_to_response(self.get_context_data(team=team, horas_formset=horas_team,
                                                                 permisos=permisos, formularios=formularios))

    def get_context_data(self, **kwargs):
        """
        Metodo que retorna un diccionario utilizado para pasar datos a las vistas
        :param kwargs: Diccionario de datos adicionales para el contexto
        :return: diccionario de contexto necesario para la correcta visualizacion de los datos
        """
        self.object = None
        context = super().get_context_data(**kwargs)
        tm_disponibles = []
        context['tm_disponibles'] = json.dumps(tm_disponibles)
        context['title'] = "Crear Sprint"
        context['project'] = Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])
        context['obs'] = "Los sprints se crean por defecto en estado Pendiente, deben iniciarse manualmente"
        context['direccion'] = {}
        context['direccion']['Ejecuciones'] = (1, '/proyectos/ejecuciones/')
        context['direccion'][str(context['project'])] = (2, '/proyectos/ejecuciones/' + str(self.kwargs['pk_proyecto']) + '/')
        context['direccion']['Sprints'] = (3, '/proyectos/ejecuciones/' + str(self.kwargs['pk_proyecto']) + '/sprints/')
        context['direccion']['Crear'] = (4, '/proyectos/ejecuciones/' + str(self.kwargs['pk_proyecto']) + '/sprints/create/')
        return context


@method_decorator(login_required, name='dispatch')
class UpdateSprintView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Vista para la modificacion de un Sprint
    """
    template_name = 'sprint/sprint.html'
    model = Sprint
    form_class = UpdateSprintForm
    success_url = '../../'
    success_message = 'Los cambios se guardaron correctamente'

    def get(self, request, *args, **kwargs):
        """
        Metodo que es ejecutado al darse una consulta GET
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta GET
        """
        self.object = self.get_object()
        permisos = request.user.get_nombres_permisos(proyecto=self.kwargs['pk_proyecto'])
        return self.render_to_response(self.get_context_data(permisos=permisos))

    def get_context_data(self, **kwargs):
        """
        Metodo que retorna un diccionario utilizado para pasar datos a las vistas
        :param kwargs: Diccionario de datos adicionales para el contexto
        :return: diccionario de contexto necesario para la correcta visualizacion de los datos
        """
        context = super().get_context_data(**kwargs)
        context['title'] = "Modificar Sprint" + str(self.object.pk)
        context['project'] = Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])
        context['dias_habiles'] = self.object.get_dias_habiles()
        horas_asignadas = Horas.objects.filter(sprint=self.object.pk)
        tm_asignados = []
        for tm in horas_asignadas:
            if tm.team_member not in tm_asignados:
                tm_asignados.append(tm.team_member)
        all_tm = TeamMember.objects.filter(proyecto=context['project'].pk)
        tm_disponibles = []
        for tm in all_tm:
            if tm.usuario not in tm_asignados:
                data = {'username': tm.usuario.username,
                        'user_pk': tm.usuario.pk}
                tm_disponibles.append(data)
        context['tm_disponibles'] = json.dumps(tm_disponibles)
        team_members = Horas.objects.filter(sprint=self.object)
        horas_data = []
        team_actual = []
        for tm in team_members:
            usuario = Usuario.objects.get(pk=tm.team_member.pk)
            h = {'team_member': tm.team_member,
                 'horas_laborales': tm.horas_laborales}
            team_actual.append(usuario)
            horas_data.append(h)
        TeamMemberFormSet = inlineformset_factory(Sprint, Horas, form=HorasForm, extra=len(horas_data))
        horas_formset = TeamMemberFormSet(initial=horas_data)
        formularios = {}
        formularios['formularios'] = {}
        readonly = False
        if self.object.estado != 'Pendiente':
            readonly = True
        for tm in horas_formset:
            tm.fields['horas_laborales'].widget.attrs['readonly'] = readonly
            if tm.get_user_id() not in formularios.keys():
                formularios[tm.get_user_id()] = {}
            formularios[tm.get_user_id()]['usuario'] = tm.get_username()
            formularios[tm.get_user_id()]['formulario'] = tm
        context['team_actual'] = team_actual
        context['horas_formset'] = horas_formset
        context['formularios'] = formularios
        context['direccion'] = {}
        context['direccion']['Ejecuciones'] = (1, '/proyectos/ejecuciones/')
        context['direccion'][str(context['project'])] = (2, '/proyectos/ejecuciones/' + str(self.kwargs['pk_proyecto']) + '/')
        context['direccion']['Sprints'] = (3, '/proyectos/ejecuciones/' + str(self.kwargs['pk_proyecto']) + '/sprints/')
        context['direccion']['Modificar: '+self.object.nombre] = (4, '/proyectos/ejecuciones/' + str(self.kwargs['pk_proyecto']) + '/sprints/modificar/'+str(self.object.pk)+'/')
        return context

    def get_object(self, queryset=None):
        """
        Metodo que retorna el objeto a ser modificado
        :param queryset:
        :return: el objeto actual
        """
        return Sprint.objects.get(pk=self.kwargs['sprint_pk'])

    def post(self, request, *args, **kwargs):
        """
        Metodo que es ejecutado al darse una consulta POST
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta POST
        """
        from usuarios.models import Usuario
        dias_habiles = str(request.POST.getlist('dias_habiles'))[1:-1].replace("'","")
        dias_habiles = dias_habiles.replace(" ","")
        permisos = request.user.get_nombres_permisos(proyecto=self.kwargs['pk_proyecto'])
        self.object = self.get_object()
        formclass = self.get_form_class()
        form = self.get_form(formclass)
        team = TeamMember.objects.filter(proyecto=self.kwargs['pk_proyecto'])
        horas_team = HorasFormSet(request.POST)
        #Reasignacion de team members
        if 'viejo_tm' in request.POST.keys() and 'tm_disponibles' in request.POST.keys():
            viejo_tm = Usuario.objects.get(pk=request.POST['viejo_tm'])
            nuevo_tm = Usuario.objects.get(pk=request.POST['tm_disponibles'])
            us_a_modificar_p = UserStory.objects.filter(team_member=viejo_tm.pk, estado=2)
            us_a_modificar_a = UserStory.objects.filter(team_member=viejo_tm.pk, estado=1)
            #Lista de todos los us a reasignar, enviar al usuario nuevo_tm
            us_a_modificar = us_a_modificar_a.union(us_a_modificar_p)
            for us in us_a_modificar:
                us.team_member = nuevo_tm
                us.save()
            horas = Horas.objects.filter(sprint=self.kwargs['sprint_pk'],team_member=viejo_tm.pk)
            for hora in horas:
                hora.team_member = nuevo_tm
                hora.save()
            # Notificación al Desarrollador por correo
            body = render_to_string(
                '../templates/notificaciones/reasignacion_us.html', {
                    # Poner los parámetros requeridos del correo
                    'lista_us': us_a_modificar,
                    'proyecto': us.proyecto.nombre,
                    'sprint': us.sprint.nombre,
                    'team_member': nuevo_tm.first_name,
                },
            )
            # email_msg = EmailMessage(
            #     subject='Asignacion de US',
            #     body=body,
            #     from_email=['PoliProyectos-noreply'],
            #     to=[nuevo_tm.email],
            # )
            # email_msg.content_subtype = 'html'
            # email_msg.send()
            return HttpResponseRedirect('./')
        #fin reasignacion de team members
        if form.is_valid() and horas_team.is_valid():
            try:
                with transaction.atomic():
                    self.object = form.save()
                    self.object.validate()
                    horas_team.instance = self.object
                    Horas.objects.filter(sprint=self.object).delete()
                    horas_team.save()
                    return HttpResponseRedirect(self.success_url)
            except ValidationError as e:
                form_error = e.message
                formularios = {}
                for ht in horas_team:
                    usuario = Usuario.objects.get(pk=ht['team_member'].value())
                    if usuario.pk not in formularios.keys():
                        formularios[usuario.pk] = {}
                    formularios[usuario.pk]['usuario'] = usuario.username
                    formularios[usuario.pk]['formulario'] = ht
                return self.render_to_response(self.get_context_data(team=team, horas_formset=horas_team,
                                                                     permisos=permisos, formularios=formularios,
                                                                     form_error=form_error))
        else:
            formularios = {}
            for ht in horas_team:
                usuario = Usuario.objects.get(pk=ht['team_member'].value())
                if usuario.pk not in formularios.keys():
                    formularios[usuario.pk] = {}
                formularios[usuario.pk]['usuario'] = usuario.username
                formularios[usuario.pk]['formulario'] = ht
            return self.render_to_response(self.get_context_data(team=team, horas_formset=horas_team,
                                                                 permisos=permisos, formularios=formularios))


@method_decorator(login_required, name='dispatch')
class AsignarUSUpdateView(LoginRequiredMixin, ListView):
    """
    Vista para la asignacion de user story
    """
    template_name = 'sprint/asignar_us.html'
    model = UserStory

    def get_queryset(self):
        """retorna la lista de todos los user stories pendientes actualmente"""
        sprint = Sprint.objects.get(pk=self.kwargs['sprint_pk'])
        asignados = UserStory.objects.filter(proyecto=self.kwargs['pk_proyecto'],
                                                estado=1, sprint=sprint.pk)
        pendientes = UserStory.objects.filter(proyecto=self.kwargs['pk_proyecto'],
                                                estado=2)
        return asignados.union(pendientes)

    def get_pendientes_clasificados(self,sprint):
        """retorna dos listas, primero una lista de todos los user stories pendientes
        que ya han sido trabajados en otro sprint ordenados por priorizacion y segundo
        la lista de todos los user stories pendientes que aun no han sido trabajados
        ordenados por priorizacion"""
        second_list_a = UserStory.objects.filter(proyecto=self.kwargs['pk_proyecto'],
                                                    sprints_asignados=None, estado=1,
                                                    sprint=sprint.pk)
        second_list_p = UserStory.objects.filter(proyecto=self.kwargs['pk_proyecto'],
                                                    sprints_asignados=None, estado=2)
        second_list = second_list_a.union(second_list_p)
        first_list = self.get_queryset().difference(second_list)
        sl = []
        for us in second_list:
            sl.append(us)
        sl.sort(key=lambda x: x.priorizacion, reverse=True)
        fl = []
        for us in first_list:
            fl.append(us)
        fl.sort(key=lambda x: x.priorizacion, reverse=True)
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
        :param kwargs: Diccionario de datos adicionales para el contexto
        :return: diccionario de contexto necesario para la correcta visualizacion de los datos
        """
        context = super(AsignarUSUpdateView,self).get_context_data(**kwargs)
        context['notas'] = {}
        context['archivos'] = {}
        context['actividades'] = {}
        for us in self.object_list:
            context['notas'][us.pk] = Nota.objects.filter(us=us.pk)
            context['archivos'][us.pk] = Archivo.objects.filter(us=us.pk)
            context['actividades'][us.pk] = Actividad.objects.filter(us=us.pk)
        context["title"] = "Asignar User Stories"
        sprint = Sprint.objects.get(pk=self.kwargs['sprint_pk'])
        fl, sl = self.get_pendientes_clasificados(sprint)
        context['second_list'] = sl
        context['first_list'] = fl
        horas = Horas.objects.filter(sprint=sprint.pk)
        team_members = []
        horas_tm = {}
        capacidad = 0
        for h in horas:
            team_member = Usuario.objects.get(pk=h.team_member.pk)
            team_members.append(team_member)
            capacidad += h.horas_laborales
        context['team_members'] = team_members
        for tm in team_members:
            if tm.username not in horas_tm.keys():
                horas_dia = Horas.objects.get(sprint=sprint.pk,team_member=tm.pk)
                dias_laborales = sprint.dias_laborales
                horas_tm[tm.pk] = dias_laborales * horas_dia.horas_laborales
        context['horas_tm'] = horas_tm
        context['capacidad_sprint'] = capacidad * sprint.dias_laborales
        context['proyecto'] = Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])
        context['sprint'] = Sprint.objects.get(pk=self.kwargs['sprint_pk'])
        proyecto = Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])
        context['direccion'] = {}
        context['direccion']['Ejecuciones'] = (1, '/proyectos/ejecuciones/')
        context['direccion'][proyecto.nombre] = (2, '/proyectos/ejecuciones/' + str(proyecto.pk) + '/')
        context['direccion']['Planificar Sprint: '+ context['sprint'].nombre] = (3,
            '/proyectos/ejecuciones/' + str(proyecto.pk) + '/sprints/'+str(context['sprint'].pk)+'/asignarus/')
        return context

    def post(self,request,*args,**kwargs):
        """Metodo que valida las asignaciones realizadas por el usuario, de ser validas guarda el user
        story asignado al sprint pendiente, de no ser validas regresa a la vista de asignacion
        para visualizar los errores
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta POST
        """
        self.object_list = self.get_queryset()
        permisos = request.user.get_nombres_permisos(proyecto=self.kwargs['pk_proyecto'])
        asigned = request.POST.getlist('user_stories')
        sprint = Sprint.objects.get(pk=self.kwargs['sprint_pk'])
        for us in self.object_list:
            if str(us.pk) in asigned:
                '''Se asignan los us al sprint'''
                us.sprint = sprint
                us.estado = 1  # asignado
                us.fase = Fase.objects.filter(flujo=us.flujo.pk).order_by('pk')[0]
                us.estado_fase = 'To Do'
                asignado_pk = request.POST['team_member_' + str(us.pk)]
                asignado = None
                if asignado_pk:
                    asignado = Usuario.objects.get(pk=asignado_pk)
                us.team_member = asignado
                us.duracion_restante = int(request.POST['duracion_estimada_' + str(us.pk)])
                try:
                    us.validate_asignacion()
                    us.save()
                except ValidationError as e:
                    error_msg = e.message
                    return self.render_to_response(self.get_context_data(permisos=permisos,
                                                                         error_msg=error_msg,
                                                                         set_team_members=True))
            else:
                '''Se quita la asignacion a todos los us que no fueron seleccionados'''
                us.duracion_estimada = request.POST['duracion_estimada_' + str(us.pk)]
                us.sprint = None
                us.fase = None
                us.estado = 2  # pendiente
                us.estado_fase = 'To Do'
                us.team_member = None
                us.save()
        return HttpResponseRedirect('../../../')

@method_decorator(login_required, name='dispatch')
class VerSprintDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    """
    Clase de la vista utilizada para visualizar los sprints sin opciones de modificacion
    """
    model = Sprint
    template_name = 'sprint/ver_sprint.html'

    def get(self, request, *args, **kwargs):
        """
        Metodo que es ejecutado al darse una consulta GET
        :param request: consulta recibida
        :param args: argumentos adicionales
        :param kwargs: diccionario de datos adicionales
        :return: la respuesta a la consulta GET
        """
        self.object = self.get_object()
        permisos = request.user.get_nombres_permisos(proyecto=self.kwargs['pk_proyecto'])
        return self.render_to_response(self.get_context_data(permisos=permisos))

    def get_context_data(self, **kwargs):
        """
        Metodo que retorna un diccionario utilizado para pasar datos a las vistas
        :param kwargs: Diccionario de datos adicionales para el contexto
        :return: diccionario de contexto necesario para la correcta visualizacion de los datos
        """
        context = super().get_context_data(**kwargs)
        context['title'] = "Ver Sprint" + str(self.object.pk)
        context['project'] = Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])
        all_us = UserStory.objects.filter(sprints_asignados__id=self.object.pk)
        context['sprint_backlog'] = []
        for us in all_us:
            context['sprint_backlog'].append(us)
        context['sprint_backlog'].sort(key=lambda x: x.priorizacion, reverse=True)
        context['notas'] = {}
        context['archivos'] = {}
        context['actividades'] = {}
        for us in all_us:
            context['notas'][us.pk] = Nota.objects.filter(us=us.pk)
            context['archivos'][us.pk] = Archivo.objects.filter(us=us.pk)
            actividades = Actividad.objects.filter(us=us.pk)
            cambios = CambioEstado.objects.filter(us=us.pk)
            context['actividades'][us.pk] = []
            for a in actividades:
                a.tipo = 'actividad'
                context['actividades'][us.pk].append(a)
            for c in cambios:
                c.tipo = 'cambio'
                context['actividades'][us.pk].append(c)
            context['actividades'][us.pk].sort(key=lambda x: x.fecha, reverse=True)
        context['direccion'] = {}
        context['direccion']['Ejecuciones'] = (1, '/proyectos/ejecuciones/')
        context['direccion'][str(context['project'])] = (2, '/proyectos/ejecuciones/' + str(self.kwargs['pk_proyecto']) + '/')
        context['direccion']['Sprints'] = (3, '/proyectos/ejecuciones/' + str(self.kwargs['pk_proyecto']) + '/sprints/')
        context['direccion']['Ver: ' + self.object.nombre] = (4, '/proyectos/ejecuciones/' + str(self.kwargs['pk_proyecto']) + '/sprints/ver/' + str(self.object.pk) + '/')
        context['dias_habiles'] = self.object.get_nombres_dias_habiles()
        context['team_members'] = Horas.objects.filter(sprint=self.object.pk)
        return context

    def get_object(self, queryset=None):
        """
        Metodo que retorna el objeto actual
        :param queryset:
        :return: el objeto actual
        """
        sprint = Sprint.objects.get(pk=self.kwargs['pk'])
        sprint.duracion_real = sprint.get_duracion_real()
        return sprint
