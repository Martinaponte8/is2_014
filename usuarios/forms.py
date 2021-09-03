
from django import forms
from django.contrib.auth.forms import SetPasswordForm

from .models import Usuario
from rol.models import Permiso

class CreateUserForm(forms.ModelForm):
    """
    Formulario para la creacion de un  Usuario
    """

    def _init_(self, *args, **kwargs):
        super(CreateUserForm, self)._init_(*args, **kwargs)
        permisos_all = Permiso.objects.filter()
        p = self.fields['permisos'].widget
        permisos = []
        for permiso in permisos_all:
            permisos.append((permiso.id, permiso.nombre))
        p.permisos = permisos

    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Usuario
        fields = ('username',
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

    def _init_(self, *args, **kwargs):
        super(UpdateUserForm, self)._init_(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['username'].widget.attrs['readonly'] = True
        permisos_all = Permiso.objects.filter()
        p = self.fields['permisos'].widget
        permisos = []
        for permiso in permisos_all:
            permisos.append((permiso.id, permiso.nombre))
        p.choices = permisos

    def clean_username(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.username
        else:
             return self.cleaned_data['username']

