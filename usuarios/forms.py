from django import forms
from django.contrib.auth.forms import SetPasswordForm

from .models import Usuario
from rol.models import Permiso

class CreateUserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
       permisos_all = Permiso.objects.filter(tipo=1)
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
        return user

class UpdateUserForm(forms.ModelForm):
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
        user = super(UpdateUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['username'].widget.attrs['readonly'] = True
         permisos_all = Permiso.objects.filter(tipo=1)
        p = self.fields['permisos'].widget
        permisos = []
         for permiso in permisos_all:
            permisos.append((permiso.id, permiso.nombre))
         p.choices = permisos

    def clean_username(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.sku
        else:
            return self.cleaned_data['username']

