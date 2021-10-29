Comentarios
============

from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .forms import *
from proyecto.forms import CreateProjectForm, UpdateProjectForm
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from sprint.models import *
from flujo.models import *
from django.utils import timezone
from userstory.models import *
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

"""
Vistas del Proyecto
"""

"""
Funcion eliminar Proyecto
"""
def eliminar2(request, project_id):
    return redirect("index")

@method_decorator(login_required, name='dispatch')
class VerProyectoDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):

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
:return: Retorna el proyecto a ser visualizado
"""
        return Proyecto.objects.get(pk=self.kwargs['pk'])


@method_decorator(login_required, name='dispatch')
class ProjectListView(LoginRequiredMixin, ListView):
"""
Clase de la vista de la lista de Proyectos
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
        return self.render_to_response(self.get_context_data(object_list=self.object_list, permisos=permisos))


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


@method_decorator(login_required, name='dispatch')
class CreateProjectView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
"""
    Clase de la vista para la creacion de un nuevo Proyecto
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
        return self.render_to_response(self.get_context_data(permisos=permisos, form=form, team_members=team_member_formset))

    def get_context_data(self, **kwargs):
"""
Metodo que retorna un diccionario utilizado para pasar datos a las vistas
"""
:param kwargs: Diccionario de datos adicionales para el contexto
"""
:return: diccionario de contexto necesario para la correcta visualizacion de los datos
"""
        context = super(CreateProjectView, self).get_context_data(**kwargs)
        return context

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
        if form.is_valid() and team_member_formset.is_valid():
            return self.form_valid(form, team_member_formset)
        else:
            return self.form_invalid(form, team_member_formset, permisos)

    def form_valid(self, form, team_member_formset):
"""
Metodo ejecutado luego de verificar que el formulario recibido en la consulta POST es valido
"""
:param form: formulario a ser guardado
"""
:param team_member_formset: grupo de team members del proyecto
"""
:return: redireccion al sucess_url de la clase
"""
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form, team_member_formset, permisos):
"""
Metodo que se ejecuta si el formulario recibido en la consulta POST es invalido
"""
:param form: formulario a ser guardado
"""
:param team_member_formset: grupo de team members del proyecto
"""
:return: redireccion a la pagina actual con los errores de validacion
"""
        if team_member_formset.vacio:
            fs_error = "Debe ingresar al menos un team member"
        if team_member_formset.sin_usuario:
            fs_error = "Debe completar el campo Usuario de todos los team members"
        if team_member_formset.sin_rol:
            fs_error = "Debe asignar un rol a todos los team members"
        if team_member_formset.doble_usuario:
            fs_error = "El usuario " + team_member_formset.doble_usuario + " se asignó mas de una vez"
        if team_member_formset.rol_doble:
            fs_error = "Solo puede existir un "+str(team_member_formset.rol_doble.nombre)
        return self.render_to_response(self.get_context_data(fs_error=fs_error, form=form, team_members=team_member_formset, permisos=permisos))


@method_decorator(login_required, name='dispatch')
class UpdateProjectView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
"""
Clase de la vista para la modificacion de un Proyecto
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
        return self.render_to_response(self.get_context_data(permisos=permisos, form=form, team_members=team_member_formset))

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
:return: El proyecto a ser modificado
"""
        return Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])

    def post(self,request,*args,**kwargs):
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
        permisos = request.user.get_nombres_permisos()
        if form.is_valid() and team_member_formset.is_valid():
            return self.form_valid(form, team_member_formset)
        else:
            return self.form_invalid(form, team_member_formset, permisos)

    def form_valid(self, form, team_member_formset):
"""
Metodo ejecutado luego de verificar que el formulario recibido en la consulta POST es valido
"""
:param form: formulario a ser guardado
"""
:param team_member_formset: grupo de team members del proyecto
"""
:return: redireccion al sucess_url de la clase
"""
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, team_member_formset, permisos):
"""
Metodo que se ejecuta si el formulario recibido en la consulta POST es invalido
"""
:param form: formulario a ser guardado
"""
:param team_member_formset: grupo de team members del proyecto
"""
:return: redireccion a la pagina actual con los errores de validacion
"""
        if team_member_formset.vacio:
            fs_error = "Debe ingresar al menos un team member"
        if team_member_formset.sin_usuario:
            fs_error = "Debe completar el campo Usuario de todos los team members"
        if team_member_formset.sin_rol:
            fs_error = "Debe asignar un rol a todos los team members"
        if team_member_formset.doble_usuario:
            fs_error = "El usuario " + team_member_formset.doble_usuario + " se asignó mas de una vez"
        if team_member_formset.rol_doble:
            fs_error = "Solo puede existir un "+str(team_member_formset.rol_doble.nombre)
        return self.render_to_response(self.get_context_data(permisos=permisos, fs_error=fs_error, form=form, team_members=team_member_formset))


"""
Vistas de Definiciones de Proyecto
"""

@method_decorator(login_required, name='dispatch')
class OptionsListView(LoginRequiredMixin, ListView):
"""
Clase de la vista de la lista de definiciones de un proyecto existente
"""
    template_name = 'proyecto/opciones_list.html'
    model = Proyecto
    queryset = Proyecto.objects.all()

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
        self.object_list = Proyecto.objects.all()
        return self.render_to_response(self.get_context_data(visibles=visibles, permisos=permisos))

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


@method_decorator(login_required, name='dispatch')
class UpdateOptionsView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
"""
Clase de la vista para modificacion de las definiciones de proyecto
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
        return self.render_to_response(self.get_context_data(permisos=permisos, form=form, team_members=team_member_formset))

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
:return: El proyecto a ser modificado
"""
        return Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])

    def post(self,request,*args,**kwargs):
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

        if form.is_valid() and team_member_formset.is_valid():
            return self.form_valid(form, team_member_formset)
        else:
            return self.form_invalid(form, team_member_formset)

    def form_valid(self, form, team_member_formset):
"""
Metodo ejecutado luego de verificar que el formulario recibido en la consulta POST es valido
"""
:param form: formulario a ser guardado
"""
:param team_member_formset: grupo de team members del proyecto
"""
:return: redireccion al sucess_url de la clase
"""

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form,team_member_formset):
"""
Metodo que se ejecuta si el formulario recibido en la consulta POST es invalido
"""
:param form: formulario a ser guardado
"""
:param team_member_formset: grupo de team members del proyecto
"""
:return: redireccion a la pagina actual con los errores de validacion
"""
        return self.render_to_response(self.get_context_data(form=form, team_members=team_member_formset))


"""
Vistas de Ejecucion
"""


@method_decorator(login_required, name='dispatch')
class EjecucionListView(LoginRequiredMixin, ListView):
"""
Clase de la vista de la lista de los proyectos en ejecucion
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

        return self.render_to_response(self.get_context_data(visibles=visibles, permisos=permisos))

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


@method_decorator(login_required, name='dispatch')
class UpdateEjecucionView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
"""
Clase de la vista para las modificaciones de los proyectos en ejecucion
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
        permisos = request.user.get_nombres_permisos(proyecto=self.kwargs['pk_proyecto'])
        return self.render_to_response(self.get_context_data(permisos=permisos))

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
        self.object = self.get_object()
        proyecto = self.get_object()
        permisos = request.user.get_nombres_permisos(proyecto=self.kwargs['pk_proyecto'])
        if 'iniciar' in request.POST.keys():
            proyecto.estado = "Activo"
            proyecto.save()
        if 'terminar' in request.POST.keys():
            proyecto.estado = "Terminado"
            proyecto.save()
        if 'suspender' in request.POST.keys():
            proyecto.estado = "Suspendido"
            proyecto.save()
        if 'cancelar' in request.POST.keys():
            proyecto.estado = "Cancelado"
            proyecto.save()
        if 'reiniciar' in request.POST.keys():
            proyecto.estado = "Activo"
            proyecto.save()
        if 'terminar_sprint' in request.POST.keys():
            sprint = Sprint.objects.get(pk=request.POST['terminar_sprint'])
            no_terminados = UserStory.objects.filter(estado=1,sprint=sprint.pk)
            if not no_terminados:
            else:
                return render(request,'proyecto/ejecucion.html',self.get_context_data(permisos=permisos, confirmar='fin_sprint'))
        if 'conf_terminar' in request.POST.keys():
            for us in us_list:
                # Notificación al Desarrollador por correo
                body = render_to_string(
                    },
                )

        if 'iniciar_sprint' in request.POST.keys():
            sprint_us = sprint.get_user_stories()
            if sprint_us:
                sprint.estado = 'En Proceso'
                for us in us_list:

                    us.estado_fase = 'To Do'
                    us.save()
            else:
                return render(self.get_context_data(error='sinus',permisos=permisos))
        return HttpResponseRedirect('./')

    def get_context_data(self, **kwargs):
"""
Metodo que retorna un diccionario utilizado para pasar datos a las vistas
"""
:param kwargs: Diccionario de datos adicionales para el contexto
"""
:return: diccionario de contexto necesario para la correcta visualizacion de los datos
"""
        context = super().get_context_data(**kwargs)
        context['title'] = "Ejecucion de Proyecto"
        try:
            context['sprint_pendiente'] = Sprint.objects.get(proyecto=self.kwargs['pk_proyecto'], estado="Pendiente")
        except:
            pass
        try:
            context['sprint_actual'] = Sprint.objects.get(proyecto=self.kwargs['pk_proyecto'], estado="En Proceso")
        except:
            pass

        return context

    def get_object(self, queryset=None):
"""
Metodo que retorna el objeto a ser modificado
"""
:param queryset:
"""
:return: Retorna el proyecto a ser modificado
"""
        return Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])


@method_decorator(login_required, name='dispatch')
class UpdateTeamMemberView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
"""
Clase de la vista para la modificacion del Team Member
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
        return self.render_to_response(self.get_context_data(permisos=permisos, form=form, team_members=team_member_formset))

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
Metodo que retorna el objeto a ser visualizado
"""
:param queryset:
"""
:return: Retorna el proyecto a ser modificado
"""
        return Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])

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

        if form.is_valid() and team_member_formset.is_valid():
            return self.form_valid(form, team_member_formset)
        else:
            return self.form_invalid(form, team_member_formset)

    def form_valid(self, form, team_member_formset):
"""
Metodo que se ejecuta si el formulario recibido en la consulta POST es valido
"""
:param form: formulario a ser guardado
"""
:param team_member_formset: grupo de team members del proyecto
"""
:return: redireccion a la direccion definida en el atributo success_url de la clase
"""
    def form_invalid(self, form, team_member_formset):
"""
Metodo que se ejecuta si el formulario recibido en la consulta POST es invalido
"""
:param form: formulario a ser guardado
"""
:param team_member_formset: grupo de team members del proyecto
"""
:return: redireccion a la pagina actual con los errores de validacion
"""
        if team_member_formset.vacio:
            fs_error = "Debe ingresar al menos un team member"
        if team_member_formset.sin_usuario:
            fs_error = "Debe completar el campo Usuario de todos los team members"
        if team_member_formset.sin_rol:
            fs_error = "Debe asignar un rol a todos los team members"
        if team_member_formset.doble_usuario:
            fs_error = "El usuario " + team_member_formset.doble_usuario + " se asignó mas de una vez"
        if team_member_formset.rol_doble:
            fs_error = "Solo puede existir un "+str(team_member_formset.rol_doble.nombre)
        return self.render_to_response(self.get_context_data(fs_error=fs_error, form=form, team_members=team_member_formset))


