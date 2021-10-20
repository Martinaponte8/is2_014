from django import forms
from .models import Cliente

class CreateClientForm(forms.ModelForm):
    """
    Formulario para la creacion de Cliente
    """
    class Meta:
        model = Cliente
        fields = ('nombre','ruc','direccion','telefono','descripcion')

class UpdateClientForm(forms.ModelForm):
    """
    Formulario para la modificacion de Cliente
    """
    class Meta:
        model = Cliente
        fields = ('nombre', 'ruc', 'direccion', 'telefono', 'descripcion')

