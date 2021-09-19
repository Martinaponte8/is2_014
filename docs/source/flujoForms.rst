Comentarios
============

from django import forms
from django.forms import inlineformset_factory
from .models import *

class CreateFlujoForm(forms.ModelForm):

"""
Formulario para la creacion de un nuevo Flujo
"""
    class Meta:
        fields = ('proyecto','nombre','descripcion')

    def __init__(self, *args, **kwargs):
        self.fields['proyecto'].widget = forms.HiddenInput()

class UpdateFlujoForm(forms.ModelForm):

"""
Formulario para la modificacion de un flujo
"""

    class Meta:
        fields = ('proyecto','nombre','descripcion')

    def __init__(self, *args, **kwargs):
        self.fields['proyecto'].widget = forms.HiddenInput()

class FaseForm(forms.ModelForm):

"""
Formulario para la creacion de una fase
"""
    class Meta:


class FaseFormSet(BaseFaseFormSet):

"""
Formulario para darle valor a una fase
"""
    def is_valid(self):
        super(FaseFormSet,self).is_valid()
"""
Retorna verdadero si existe al menos un formulario dentro del formset ytodos los formularios en el formset tienen nombre, en caso contrario retorna falso
"""
        self.vacio = False
        self.sin_nombre = False
        if not self.forms:
            self.vacio = True
            return False
        for form in self.forms:
            if not str(form['nombre'].value()).strip():
                self.sin_nombre = True
                return False
        if not self.is_bound:
            return False
        return True

