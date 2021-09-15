from django import forms
from .models import *
# from .models import Nota

class CreateUserStoryForm(forms.ModelForm):
    """
    Formulario de la creacion de User Story
    """
    class Meta:
        model = UserStory
        fields = ('proyecto',
                  'nombre',
                  'descripcion',
                  'duracion_estimada',
                  'valor_negocio',
                  'prioridad',
                  'valor_tecnico',
                  'tipo_us',
                  'flujo',
                  )

        widgets = {
            'proyecto': forms.HiddenInput,
        }

class UpdateUserStoryForm(forms.ModelForm):
    """
    Formulario de la modificacion de User Story
    """
    class Meta:
        model = UserStory
        fields = ('proyecto',
                  'nombre',
                  'descripcion',
                  'duracion_estimada',
                  'valor_negocio',
                  'prioridad',
                  'valor_tecnico',
                  'tipo_us',
                  'flujo',
                  )

        widgets ={
            'proyecto': forms.HiddenInput,
        }


# class ArchivoForm(forms.ModelForm):
#     """
#     Formulario para subir archivos al User Story
#     """
#     class Meta:
#         model = Archivo
#         """Campos a ingresar"""
#         fields = ('titulo', 'archivo', )


# class NotaForm(forms.ModelForm):
#     """
#     Formulario para subir notas al User Story
#     """
#     class Meta:
#         model = Nota
#         """Campos a ingresar"""
#         fields = ('nota',)


# class ActividadForm(forms.ModelForm):
#     """
#     Formulario para agregar actividades al User Story
#     """
#     class Meta:
#         model = Actividad
#         """Campos a ingresar"""
#         fields = ('nombre','descripcion','duracion')


# class GuardarNotaForm(forms.ModelForm):
#     """
#     Formulario para guardar notas en el user story
#     """
#     class Meta:
#         model = Nota
#         """Campos a ingresar"""
#         fields = ('us', 'usuario', 'nota','sprint')


# class GuardarArchivoForm(forms.ModelForm):
#     """
#     Formulario para guardar archivos en el User Story
#     """
#     class Meta:
#         model = Archivo
#         """Campos a ingresar"""
#         fields = ('titulo', 'archivo','us','usuario','sprint')
#
#
# class GuardarActividadForm(forms.ModelForm):
#     """
#     Formulario para guardar actividades en el User Story
#     """
#     class Meta:
#         model = Actividad
#         """Campos a ingresar"""
#         fields = ('nombre','descripcion','duracion','us','usuario','sprint','fase_us','estado_fase')
