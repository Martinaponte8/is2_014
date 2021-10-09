Comentarios
============

from rol.models import *
from django import forms


class CreateRolForm(forms.ModelForm):

"""
    Formulario para crear un Rol
"""
    class Meta:
        model = Rol
        fields = [
            'nombre',
            'is_unique',
            'descripcion',
            'permisos'
        ]
        labels = {
            'nombre': 'Nombre del rol',
            'descripcion': 'Descripcion ',
            'permisos': 'Permisos',

        }
        widgets = {
            'permisos': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(CreateRolForm, self).__init__(*args, **kwargs)
        permisos_all = Permiso.objects.filter(tipo=2)
        p = self.fields['permisos'].widget
        permisos = []
        for permiso in permisos_all:
            permisos.append((permiso.id, permiso.nombre))
        p.choices = permisos

    def clean_permiso(self):
        permisos = self.cleaned_data['permisos']
        try:
            pr = Permiso.objects.get(permisos=permisos)
        except:
            return self.cleaned_data['permisos']
        raise forms.ValidationError('Debe seleccionar al menos uno')


class UpdateRolForm(forms.ModelForm):
"""
    Formulario para modificar un Rol
"""
    class Meta:
        model = Rol
        fields = [
            'nombre',
            'is_unique',
            'descripcion',
            'permisos'
        ]
        labels = {
            'nombre': 'Nombre del rol',
            'descripcion': 'Descripcion ',
            'permisos': 'Permisos',

        }
        widgets = {
        'permisos': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(UpdateRolForm, self).__init__(*args, **kwargs)
        permisos_all = Permiso.objects.filter(tipo=2)
        p = self.fields['permisos'].widget
        permisos = []
        for permiso in permisos_all:
            permisos.append((permiso.id, permiso.nombre))
        p.choices = permisos

    def clean_permiso(self):
        permisos = self.cleaned_data['permisos']
        try:
            pr = Permiso.objects.get(permisos=permisos)
        except:
            return self.cleaned_data['permisos']
        raise forms.ValidationError('Debe seleccionar al menos uno')