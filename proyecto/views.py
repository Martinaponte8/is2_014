

from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .forms import *
from proyecto.forms import CreateProjectForm, UpdateProjectForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from sprint.models import *
from flujo.models import *
from django.utils import timezone
from userstory.models import *

from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from .models import *
from .forms import *
from proyecto.forms import CreateProjectForm, UpdateProjectForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden,HttpResponseRedirect
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from sprint.models import *
from flujo.models import *
from django.utils import timezone
from userstory.models import *
from .models import Proyecto

"""
Vistas del Proyecto
"""

"""
Funcion eliminar Proyecto
"""

def eliminar2(request, project_id):
    project = Proyecto.objects.get(id=project_id)
    project.delete()
    return redirect("index")

@method_decorator(login_required, name='dispatch')
class ProjectListView(LoginRequiredMixin, ListView):
    """
    Vista de la lista de Proyectos
    """
    template_name = 'proyecto/list.html'
    model = Proyecto
    queryset = Proyecto.objects.all()

    def get(self,request,*args,**kwargs):
        self.object_list = Proyecto.objects.all()
        permisos = request.user.get_nombres_permisos()
        return self.render_to_response(self.get_context_data(object_list=self.object_list, permisos=permisos))


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Administración de Proyectos"
        return context


@method_decorator(login_required, name='dispatch')
class CreateProjectView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """
    Vista de la creacion de un nuevo Proyecto
    """
    template_name = 'proyecto/proyecto.html'
    model = Proyecto
    success_url = '/proyectos/'
    form_class = CreateProjectForm
    success_message = 'Se ha creado el proyecto'

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        team_member_formset = TeamMemberFormSet()
        permisos = request.user.get_nombres_permisos()
        return self.render_to_response(self.get_context_data(permisos=permisos, form=form, team_members=team_member_formset))

    def get_context_data(self, **kwargs):
        context = super(CreateProjectView, self).get_context_data(**kwargs)
        context['title'] = "Crear Proyecto"
        context['obs'] = "El proyecto se crea por defecto en estado pendiente, debe iniciar el proyecto manualmente"
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        team_member_formset = TeamMemberFormSet(request.POST)

        if form.is_valid() and team_member_formset.is_valid():
            return self.form_valid(form, team_member_formset)
        else:
            return self.form_invalid(form, team_member_formset)

    def form_valid(self, form, team_member_formset):
        self.object = form.save()
        team_member_formset.instance = self.object
        team_member_formset.save()
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form, team_member_formset):
        return self.render_to_response(self.get_context_data(form=form, team_members=team_member_formset))


@method_decorator(login_required, name='dispatch')
class UpdateProjectView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Vista de la modificacion de un Proyecto
    """
    template_name = 'proyecto/proyecto.html'
    model = Proyecto
    form_class = UpdateProjectForm
    success_url = '/proyectos/'
    success_message = 'Los cambios se guardaron correctamente'

    def get(self,request,*args,**kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        team_members = TeamMember.objects.filter(proyecto=self.object).order_by('pk')
        tm_data = []
        for tm in team_members:
            d = {'usuario': tm.usuario,
                 'rol': tm.rol}
            tm_data.append(d)
        TeamMemberFormSet = inlineformset_factory(Proyecto, TeamMember, form=TeamMemberForm, extra=len(tm_data))
        team_member_formset = TeamMemberFormSet(initial=tm_data)
        permisos = request.user.get_nombres_permisos()
        return self.render_to_response(self.get_context_data(permisos=permisos, form=form, team_members=team_member_formset))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modificar Proyecto"
        return context

    def get_object(self, queryset=None):
        return Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])

    def get_absolute_url(self):
        return reverse('update_project', kwargs={'pk_proyecto': self.kwargs['pk_proyecto']})

    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        team_member_formset = TeamMemberFormSet(request.POST)
        if form.is_valid() and team_member_formset.is_valid():
            return self.form_valid(form, team_member_formset)
        else:
            return self.form_invalid(form, team_member_formset)

    def form_valid(self, form, team_member_formset):
        self.object = form.save()
        team_member_formset.instance = self.object
        TeamMember.objects.filter(proyecto=self.object).delete()
        team_member_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, team_member_formset):
        if team_member_formset.vacio:
            fs_error = "Debe ingresar al menos un team member"
        if team_member_formset.sin_usuario:
            fs_error = "Debe completar el campo Usuario de todos los team members"
        if team_member_formset.sin_rol:
            fs_error = "Debe asignar un rol a todos los team members"
        if team_member_formset.doble_usuario:
            fs_error = "El usuario " + team_member_formset.doble_usuario + " se asignó mas de una vez"
        return self.render_to_response(self.get_context_data(fs_error=fs_error, form=form, team_members=team_member_formset))


"""
Vistas de Opciones de Proyecto
"""

@method_decorator(login_required, name='dispatch')
class OptionsListView(LoginRequiredMixin, ListView):
    """
    Vista de la lista de opciones para administrar un proyecto existente
    """
    template_name = 'proyecto/opciones_list.html'
    model = Proyecto
    queryset = Proyecto.objects.all()

    def get(self,request,*args,**kwargs):
        self.object_list = Proyecto.objects.all()
        permisos = request.user.get_nombres_permisos()
        return self.render_to_response(self.get_context_data(object_list=self.object_list, permisos=permisos))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Opciones de Proyectos"
        return context

"""
Actualizar la opciones de vista
"""
@method_decorator(login_required, name='dispatch')
class UpdateOptionsView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Vistas para modificacion de las opciones de proyecto
    """
    template_name = 'proyecto/options.html'
    model = Proyecto
    form_class = UpdateProjectForm
    success_url = '/proyectos/opciones/'
    success_message = 'Los cambios se guardaron correctamente'

    def get(self,request,*args,**kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        team_members = TeamMember.objects.filter(proyecto=self.object).order_by('pk')
        tm_data = []
        for tm in team_members:
            d = {'usuario': tm.usuario,
                 'rol': tm.rol}
            tm_data.append(d)
        TeamMemberFormSet = inlineformset_factory(Proyecto, TeamMember, form=TeamMemberForm,extra=len(tm_data))
        team_member_formset = TeamMemberFormSet(initial=tm_data)
        permisos = request.user.get_nombres_permisos(proyecto=self.kwargs['pk_proyecto'])
        print(str(permisos))
        return self.render_to_response(self.get_context_data(permisos=permisos, form=form, team_members=team_member_formset))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modificar Proyecto"
        return context

    def get_object(self, queryset=None):
        return Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])

    def get_absolute_url(self):
        return reverse('update_options', kwargs={'pk_proyecto': self.kwargs['pk_proyecto']})

    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        team_member_formset = TeamMemberFormSet(request.POST)
        if form.is_valid() and team_member_formset.is_valid():
            return self.form_valid(form, team_member_formset)
        else:
            return self.form_invalid(form, team_member_formset)

    def form_valid(self, form, team_member_formset):
        self.object = form.save()
        team_member_formset.instance = self.object
        TeamMember.objects.filter(proyecto=self.object).delete()
        team_member_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form,team_member_formset):
        return self.render_to_response(self.get_context_data(form=form, team_members=team_member_formset))

"""
Vistas de Ejecucion
"""


@method_decorator(login_required, name='dispatch')
class EjecucionListView(LoginRequiredMixin, ListView):
    """
    Vista de la lista de los proyectos en ejecucion
    """
    template_name = 'proyecto/ejecuciones_list.html'
    model = Proyecto
    queryset = Proyecto.objects.all()

    def get(self, request, *args, **kwargs):
        self.object_list = Proyecto.objects.all()
        permisos = request.user.get_nombres_permisos()
        return self.render_to_response(self.get_context_data(object_list=self.object_list, permisos=permisos))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Ejecuciones de Proyectos"
        return context

"""
Actualiza la vista de ejecucion
"""
@method_decorator(login_required, name='dispatch')
class UpdateEjecucionView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Vista de las modificaciones de los proyectos en ejecucion
    """
    template_name = 'proyecto/ejecucion.html'
    model = Proyecto
    form_class = UpdateProjectForm
    success_url = '/proyectos/ejecuciones/'
    success_message = 'Los cambios se guardaron correctamente'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        formclass = self.get_form_class()
        form = self.get_form(formclass)
        permisos = request.user.get_nombres_permisos(proyecto=self.kwargs['pk_proyecto'])
        print(str(permisos))
        return self.render_to_response(self.get_context_data(form=form, permisos=permisos))

    """
    Cambiar el estado de un proyecto
    Opciones = Iniciar - Terminar -Suspender - Cancelar - Reiniciar
    """
    def post(self, request, *args, **kwargs):
        #se debe iniciar el proyecto
        proyecto = self.get_object()
        if 'iniciar' in request.POST.keys():
            proyecto.fecha_inicio = timezone.now().today()
            proyecto.estado = "Activo"
            proyecto.save()
        if 'terminar' in request.POST.keys():
            proyecto.fecha_fin = timezone.now().today()
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
        print(str(request.POST))
        if 'terminar_sprint' in request.POST.keys():
            sprint = Sprint.objects.get(pk=request.POST['terminar_sprint'])
            sprint.estado = 'Terminado'
            sprint.fecha_fin = timezone.now().today()
            sprint.save()
            us_list = UserStory.objects.filter(sprint=sprint.pk)
            for us in us_list:
                if us.estado != 0: #terminado
                    us.estado = 2 #pendiente
                    us.sprint = None
                    us.save()
        return HttpResponseRedirect('./')

    def get_context_data(self, **kwargs):
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
        flujos = Flujo.objects.filter(proyecto=self.kwargs['pk_proyecto'])
        context['flujos'] = flujos
        context['project'] = Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])
        return context

    def get_object(self, queryset=None):
        return Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])

"""
Actualiza el team Member 
"""

@method_decorator(login_required, name='dispatch')
class UpdateTeamMemberView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Vista de la modificacion del TeamMember
    """
    template_name = 'proyecto/asignacion_roles.html'
    model = Proyecto
    form_class = UpdateProjectForm
    success_url = '../'
    success_message = 'Los cambios se guardaron correctamente'

    def get(self,request,*args,**kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        team_members = TeamMember.objects.filter(proyecto=self.object).order_by('pk')
        tm_data = []
        for tm in team_members:
            d = {'usuario': tm.usuario,
                 'rol': tm.rol}
            tm_data.append(d)
        TeamMemberFormSet = inlineformset_factory(Proyecto, TeamMember, form=TeamMemberForm, extra=len(tm_data))
        team_member_formset = TeamMemberFormSet(initial=tm_data)
        permisos = request.user.get_nombres_permisos(proyecto=self.kwargs['pk_proyecto'])
        return self.render_to_response(self.get_context_data(permisos=permisos, form=form, team_members=team_member_formset))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Asignar Roles"
        return context

    def get_object(self, queryset=None):
        return Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])

    def get_absolute_url(self):
        return reverse('update_project', kwargs={'pk_proyecto': self.kwargs['pk_proyecto']})

    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        team_member_formset = TeamMemberFormSet(request.POST)
        if form.is_valid() and team_member_formset.is_valid():
            return self.form_valid(form, team_member_formset)
        else:
            return self.form_invalid(form, team_member_formset)

    def form_valid(self, form, team_member_formset):
        self.object = form.save()
        team_member_formset.instance = self.object
        TeamMember.objects.filter(proyecto=self.object).delete()
        team_member_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, team_member_formset):
        if team_member_formset.vacio:
            fs_error = "Debe ingresar al menos un team member"
        if team_member_formset.sin_usuario:
            fs_error = "Debe completar el campo Usuario de todos los team members"
        if team_member_formset.sin_rol:
            fs_error = "Debe asignar un rol a todos los team members"
        if team_member_formset.doble_usuario:
            fs_error = "El usuario " + team_member_formset.doble_usuario + " se asignó mas de una vez"
        return self.render_to_response(self.get_context_data(fs_error=fs_error, form=form, team_members=team_member_formset))

@method_decorator(login_required, name='dispatch')
class VerProyectoDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = Proyecto
    template_name = 'proyecto/ver_proyecto.html'

    def get(self,request,*args,**kwargs):
        self.object = self.get_object()
        permisos = request.user.get_nombres_permisos()
        return self.render_to_response(self.get_context_data(permisos=permisos))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Ver Proyecto"
        return context

    def get_object(self, queryset=None):
        return Proyecto.objects.get(pk=self.kwargs['pk'])
