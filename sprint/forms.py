from django import forms
from .models import *
from django.forms import inlineformset_factory
from usuarios.models import *


class CreateSprintForm(forms.ModelForm):
    """
    Formulario utilizado para la creacion de un nuevo Sprint
    """
    class Meta:
        """
        Clase en la que se definen los datos necesarios y adicionales para inicializacion y
        visualizacion del formulario
        """
        model = Sprint
        fields = ('proyecto', 'nombre', 'dias_laborales','dias_habiles')

        widgets = {
            'proyecto': forms.HiddenInput(),
            'dias_habiles': forms.HiddenInput(),
        }


class UpdateSprintForm(forms.ModelForm):
    """
    Formulario utilizado para la modificacion de un Sprint
    """
    class Meta:
        """
        En esta clase se definen los datos necesarios y adicionales para inicializacion y
        visualizacion del formulario
        """
        model = Sprint
        fields = ('proyecto','nombre', 'dias_laborales','dias_habiles')

        widgets = {
            'proyecto': forms.HiddenInput(),
            'dias_habiles': forms.HiddenInput(),
        }

class HorasForm(forms.ModelForm):
    """
    Formulario para la asignacion de dias laborales
    """
    class Meta:
        """
        En esta clase se definen los datos necesarios y adicionales para inicializacion y
        visualizacion del formulario
        """
        model = Horas
        exclude = ()
        fields = ('team_member', 'horas_laborales',)


    def get_username(self):
        """retorna el username del team member"""
        return Usuario.objects.get(id=self.initial['team_member'].pk).username

    def get_user_id(self):
        """retorna el username del team member"""
        return Usuario.objects.get(id=self.initial['team_member'].pk).pk


HorasFormSet = inlineformset_factory(Sprint, Horas, form=HorasForm, extra=7)
