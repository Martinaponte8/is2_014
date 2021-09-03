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
class UpdateOptionsView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Vista de modificar Proyectos
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
        detalles = ProyectoDetalle.objects.filter(proyecto=self.object).order_by('pk')
        detalles_data = []
        for detalle in detalles:
            d = {'usuario': detalle.usuario,
                 'rol': detalle.rol}
            detalles_data.append(d)
        ProyectoDetalleFormSet = inlineformset_factory(Proyecto, ProyectoDetalle, form=ProyectoDetalleForm,extra=len(detalles_data))
        proyectodetalle_orden_formset = ProyectoDetalleFormSet(initial=detalles_data)
        return self.render_to_response(self.get_context_data(form=form, proyectodetalles=proyectodetalle_orden_formset))

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
        proyectodetalle_formset = ProyectoDetalleFormSet(request.POST)
        if form.is_valid() and proyectodetalle_formset.is_valid():
            return self.form_valid(form, proyectodetalle_formset)
        else:
            return self.form_invalid(form, proyectodetalle_formset)

    def form_valid(self, form, proyectodetalle_formset):
        self.object = form.save()
        proyectodetalle_formset.instance = self.object
        ProyectoDetalle.objects.filter(proyecto=self.object).delete()
        proyectodetalle_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form,proyectodetalle_formset):
        return self.render_to_response(self.get_context_data(form=form, proyectodetalles=proyectodetalle_formset))

@method_decorator(login_required, name='dispatch')
class FlujoListView(LoginRequiredMixin, ListView):
    template_name = 'proyecto/flujo_list.html'
    model = Flujo
    queryset = Flujo.objects.all()

    def get(self,request,*args,**kwargs):
        self.object = None
        self.object_list = Flujo.objects.filter(proyecto=self.kwargs['pk_proyecto'])
        proyecto = Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])
        return self.render_to_response(self.get_context_data(project=proyecto,object_list=self.object_list))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Flujos de Proyecto"
        return context


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
        detalles = ProyectoDetalle.objects.filter(proyecto=self.object).order_by('pk')
        detalles_data = []
        for detalle in detalles:
            d = {'usuario': detalle.usuario,
                 'rol': detalle.rol}
            detalles_data.append(d)
        ProyectoDetalleFormSet = inlineformset_factory(Proyecto, ProyectoDetalle, form=ProyectoDetalleForm,extra=len(detalles_data))
        proyectodetalle_orden_formset = ProyectoDetalleFormSet(initial=detalles_data)
        return self.render_to_response(self.get_context_data(form=form, proyectodetalles=proyectodetalle_orden_formset))

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
        proyectodetalle_formset = ProyectoDetalleFormSet(request.POST)
        if form.is_valid() and proyectodetalle_formset.is_valid():
            return self.form_valid(form, proyectodetalle_formset)
        else:
            return self.form_invalid(form, proyectodetalle_formset)

    def form_valid(self, form, proyectodetalle_formset):
        self.object = form.save()
        proyectodetalle_formset.instance = self.object
        ProyectoDetalle.objects.filter(proyecto=self.object).delete()
        proyectodetalle_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form,proyectodetalle_formset):
        return self.render_to_response(self.get_context_data(form=form, proyectodetalles=proyectodetalle_formset))

@method_decorator(login_required, name='dispatch')
class FlujoListView(LoginRequiredMixin, ListView):
    template_name = 'proyecto/flujo_list.html'
    model = Flujo
    queryset = Flujo.objects.all()

    def get(self,request,*args,**kwargs):
        self.object = None
        self.object_list = Flujo.objects.filter(proyecto=self.kwargs['pk_proyecto'])
        proyecto = Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])
        return self.render_to_response(self.get_context_data(project=proyecto,object_list=self.object_list))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Flujos de Proyecto"
        return context

@method_decorator(login_required, name='dispatch')
class ProjectListView(LoginRequiredMixin, ListView):
    template_name = 'proyecto/list.html'
    model = Proyecto
    queryset = Proyecto.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Proyectos"
        return context

@method_decorator(login_required, name='dispatch')
class OptionsListView(LoginRequiredMixin, ListView):
    template_name = 'proyecto/opciones_list.html'
    model = Proyecto
    queryset = Proyecto.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Opciones de Proyectos"
        return context

"""
Vistas de Ejecucion
"""

@method_decorator(login_required, name='dispatch')
class EjecucionListView(LoginRequiredMixin, ListView):
    template_name = 'proyecto/ejecuciones_list.html'
    model = Proyecto
    queryset = Proyecto.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Ejecuciones de Proyectos"
        return context

@method_decorator(login_required, name='dispatch')
class CreateFlujoView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'proyecto/flujo.html'
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
        return self.render_to_response(self.get_context_data(form=form, fases=fases_orden_formset))

    def get_context_data(self, **kwargs):
        context = super(CreateFlujoView,self).get_context_data(**kwargs)
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
        return self.render_to_respose(self.get_context_data(form=form,fases=fases_formset))

@method_decorator(login_required, name='dispatch')
class CreateProjectView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'proyecto/proyecto.html'
    model = Proyecto
    success_url = '/proyectos/'
    form_class = CreateProjectForm
    success_message = 'Se ha creado el proyecto'

    def get(self,request,*args,**kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        proyectodetalle_orden_formset = ProyectoDetalleFormSet()
        return self.render_to_response(self.get_context_data(form=form, proyectodetalles=proyectodetalle_orden_formset))

    def get_context_data(self, **kwargs):
        context = super(CreateProjectView,self).get_context_data(**kwargs)
        context['title'] = "Crear Proyecto"
        return context

    def post(self,request,*args,**kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form()
        proyectodetalle_formset = ProyectoDetalleFormSet(request.POST)

        if form.is_valid() and proyectodetalle_formset.is_valid():
            return self.form_valid(form,proyectodetalle_formset)
        else:
            return self.form_invalid(form,proyectodetalle_formset)

    def form_valid(self, form, proyectodetalle_formset):
        self.object = form.save()
        proyectodetalle_formset.instance = self.object
        proyectodetalle_formset.save()
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form,proyectodetalle_formset):
        return self.render_to_respose(self.get_context_data(form=form,proyectodetalles=proyectodetalle_formset))


@method_decorator(login_required, name='dispatch')
class UpdateProjectView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'proyecto/proyecto.html'
    model = Proyecto
    form_class = UpdateProjectForm
    success_url = '/proyectos/'
    success_message = 'Los cambios se guardaron correctamente'

    def get(self,request,*args,**kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        detalles = ProyectoDetalle.objects.filter(proyecto=self.object).order_by('pk')
        detalles_data = []
        for detalle in detalles:
            d = {'usuario': detalle.usuario,
                 'rol': detalle.rol}
            detalles_data.append(d)
        ProyectoDetalleFormSet = inlineformset_factory(Proyecto, ProyectoDetalle, form=ProyectoDetalleForm,extra=len(detalles_data))
        proyectodetalle_orden_formset = ProyectoDetalleFormSet(initial=detalles_data)
        return self.render_to_response(self.get_context_data(form=form, proyectodetalles=proyectodetalle_orden_formset))

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
        proyectodetalle_formset = ProyectoDetalleFormSet(request.POST)
        if form.is_valid() and proyectodetalle_formset.is_valid():
            return self.form_valid(form,proyectodetalle_formset)
        else:
            return self.form_invalid(form,proyectodetalle_formset)

    def form_valid(self, form, proyectodetalle_formset):
        self.object = form.save()
        proyectodetalle_formset.instance = self.object
        ProyectoDetalle.objects.filter(proyecto=self.object).delete()
        proyectodetalle_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form,proyectodetalle_formset):
        return self.render_to_response(self.get_context_data(form=form, proyectodetalles=proyectodetalle_formset))


@method_decorator(login_required, name='dispatch')
class UpdateFlujoView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'proyecto/flujo.html'
    model = Flujo
    success_url = '../'
    form_class = CreateFlujoForm
    success_message = 'Se ha modificado el flujo'

    def get(self,request,*args,**kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        fases = Fase.objects.filter(flujo=self.object).order_by('pk')
        fases_data = []
        for fase in fases:
            d = {'nombre': fase.nombre,}
            fases_data.append(d)
        FaseFormSet = inlineformset_factory(Flujo, Fase, form=FaseForm,extra=len(fases_data))
        fases_orden_formset = FaseFormSet(initial=fases_data)
        return self.render_to_response(self.get_context_data(form=form, fases=fases_orden_formset))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modificar Flujo"
        return context

    def get_object(self, queryset=None):
        return Flujo.objects.get(pk=self.kwargs['pk'])

    def get_absolute_url(self):
        return reverse('update_project', kwargs={'pk_proyecto': self.kwargs['pk_proyecto']})

    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
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
        Fase.objects.filter(flujo=self.object).delete()
        fases_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form,fases_formset):
        return self.render_to_response(self.get_context_data(form=form, fases=fases_formset))

@method_decorator(login_required, name='dispatch')
class UpdateDetalleProyectoView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'proyecto/asignacion_roles.html'
    model = Proyecto
    form_class = UpdateProjectForm
    success_url = '../'
    success_message = 'Los cambios se guardaron correctamente'

    def get(self,request,*args,**kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        detalles = ProyectoDetalle.objects.filter(proyecto=self.object).order_by('pk')
        detalles_data = []
        for detalle in detalles:
            d = {'usuario': detalle.usuario,
                 'rol': detalle.rol}
            detalles_data.append(d)
        ProyectoDetalleFormSet = inlineformset_factory(Proyecto, ProyectoDetalle, form=ProyectoDetalleForm,extra=len(detalles_data))
        proyectodetalle_orden_formset = ProyectoDetalleFormSet(initial=detalles_data)
        return self.render_to_response(self.get_context_data(form=form, proyectodetalles=proyectodetalle_orden_formset))

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
        proyectodetalle_formset = ProyectoDetalleFormSet(request.POST)
        if form.is_valid() and proyectodetalle_formset.is_valid():
            return self.form_valid(form,proyectodetalle_formset)
        else:
            return self.form_invalid(form,proyectodetalle_formset)

    def form_valid(self, form, proyectodetalle_formset):
        self.object = form.save()
        proyectodetalle_formset.instance = self.object
        ProyectoDetalle.objects.filter(proyecto=self.object).delete()
        proyectodetalle_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form,proyectodetalle_formset):
        return self.render_to_response(self.get_context_data(form=form, proyectodetalles=proyectodetalle_formset))


@method_decorator(login_required, name='dispatch')
class UpdateProjectView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'proyecto/proyecto.html'
    model = Proyecto
    form_class = UpdateProjectForm
    success_url = '/proyectos/'
    success_message = 'Los cambios se guardaron correctamente'

    def get(self,request,*args,**kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        detalles = ProyectoDetalle.objects.filter(proyecto=self.object).order_by('pk')
        detalles_data = []
        for detalle in detalles:
            d = {'usuario': detalle.usuario,
                 'rol': detalle.rol}
            detalles_data.append(d)
        ProyectoDetalleFormSet = inlineformset_factory(Proyecto, ProyectoDetalle, form=ProyectoDetalleForm,extra=len(detalles_data))
        proyectodetalle_orden_formset = ProyectoDetalleFormSet(initial=detalles_data)
        return self.render_to_response(self.get_context_data(form=form, proyectodetalles=proyectodetalle_orden_formset))

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
        proyectodetalle_formset = ProyectoDetalleFormSet(request.POST)
        if form.is_valid() and proyectodetalle_formset.is_valid():
            return self.form_valid(form,proyectodetalle_formset)
        else:
            return self.form_invalid(form,proyectodetalle_formset)

    def form_valid(self, form, proyectodetalle_formset):
        self.object = form.save()
        proyectodetalle_formset.instance = self.object
        ProyectoDetalle.objects.filter(proyecto=self.object).delete()
        proyectodetalle_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form,proyectodetalle_formset):
        return self.render_to_response(self.get_context_data(form=form, proyectodetalles=proyectodetalle_formset))


@method_decorator(login_required, name='dispatch')
class UpdateEjecucionView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'proyecto/ejecucion.html'
    model = Proyecto
    form_class = UpdateProjectForm
    success_url = '/proyectos/ejecuciones/'
    success_message = 'Los cambios se guardaron correctamente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Ejecucion de Proyecto"
        return context

    def get_object(self, queryset=None):
        return Proyecto.objects.get(pk=self.kwargs['pk_proyecto'])

    def get_absolute_url(self):
        return reverse('update_ejecucion', kwargs={'pk_proyecto': self.kwargs['pk_proyecto']})
