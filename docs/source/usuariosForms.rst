Comentarios
============

from django import forms
from .models import Usuario
from rol.models import Permiso

class CreateUserForm(forms.ModelForm):

"""
    Formulario para la creacion de un  Usuario
"""
    class Meta:
        model = Usuario
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'estado',
                  'ci',
                  'telefono',
                  'direccion',
                  'descripcion',
                  'password',
                  'permisos'
                  )
        widgets = {
            'permisos': forms.CheckboxSelectMultiple(),
            'password': forms.PasswordInput()
        }


    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            self.save_m2m()
        return user


class UpdateUserForm(forms.ModelForm):

"""
    Formulario para la modificacion de un Usuario
"""
    class Meta:
        model = Usuario
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'estado',
                  'ci',
                  'telefono',
                  'direccion',
                  'descripcion',
                  'password',
                  'permisos'
                  )

        widgets = {
            'permisos': forms.CheckboxSelectMultiple(),
            'password': forms.PasswordInput()
        }

    def save(self, commit=True):
        user = super(UpdateUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            self.save_m2m()
        return user

    def clean_username(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.username
        else:
            return self.cleaned_data['username']