from django import forms
from django.forms import inlineformset_factory
from .models import *

class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ('nombre', 'fecha_inicio', 'fecha_fin', 'estado', 'descripcion')

    widgets = {
        'fecha_inicio': forms.DateTimeField(),
        'fecha_fin': forms.DateTimeField()
    }

    labels = {
        'nombre': 'Nombre del Proyecto',
        'fecha_inicio': 'Fecha de Inicio',
        'fecha_fin': 'Fecha de Fin',
        'estado': 'Estado',
        'descripcion': 'Descripcion ',

    }


class UpdateProjectForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ('nombre', 'fecha_inicio', 'fecha_fin', 'estado', 'descripcion')

    widgets = {
        'fecha_inicio': forms.DateTimeField(),
        'fecha_fin': forms.DateTimeField()
    }

    labels = {
        'nombre': 'Nombre del Proyecto',
        'fecha_inicio': 'Fecha de Inicio',
        'fecha_fin': 'Fecha de Fin',
        'estado': 'Estado',
        'descripcion': 'Descripcion ',

    }

class CreateFlujoForm(forms.ModelForm):
    class Meta:
        model = Flujo
        fields = ('nombre','proyecto','descripcion')
    widgets = {
        'proyecto': forms.HiddenInput()
    }

class UpdateFlujoForm(forms.ModelForm):
    class Meta:
        model = Flujo
        fields = ('nombre','proyecto','descripcion')
    widgets = {
        'proyecto': forms.HiddenInput()
    }


class ProyectoDetalleForm(forms.ModelForm):
   class Meta:
        model = ProyectoDetalle
        exclude = ()
        fields = ('usuario','rol')


class FaseForm(forms.ModelForm):
    class Meta:
        model = Fase
        exclude = ()
        fields = ('nombre',)

ProyectoDetalleFormSet = inlineformset_factory(Proyecto,ProyectoDetalle,form=ProyectoDetalleForm,extra=1)
FaseFormSet = inlineformset_factory(Flujo,Fase,form=FaseForm,extra=1)



