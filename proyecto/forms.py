from django import forms
from django.forms import inlineformset_factory

from usuarios.models import Usuario
from .models import *

class CreateProjectForm(forms.ModelForm):
    """
    Formulario para la creacion de un nuevo Proyecto
    """
    class Meta:
        model = Proyecto
        fields = ('nombre', 'fecha_ini_estimada', 'fecha_fin_estimada', 'descripcion')

    widgets = {
        'fecha_ini_estimada': forms.DateField(),
        'fecha_fin_estimada': forms.DateField()
    }


class UpdateProjectForm(forms.ModelForm):
    """
    Formulario para la modificacion de un Proyecto
    """
    class Meta:
        model = Proyecto
        fields = ('nombre', 'fecha_ini_estimada', 'fecha_fin_estimada', 'descripcion')

    widgets = {
        'fecha_ini_estimada': forms.DateField(),
        'fecha_fin_estimada': forms.DateField()
    }


class TeamMemberForm(forms.ModelForm):
    """
    Formulario para la creacion de los "Miembros del equipo"
    """
    class Meta:
        model = TeamMember
        exclude = ()
        fields = ('usuario', 'rol')


BaseTeamMemberFormSet = inlineformset_factory(Proyecto, TeamMember, form=TeamMemberForm, extra=1)

class TeamMemberFormSet(BaseTeamMemberFormSet):
    """
    Formulario para la validacion de los campos del TeamMember
    """
    def is_valid(self):
        """Retorna verdadero si existe al menos un formulario dentro del formset y todos los
        formularios en el formset tienen usuario y rol, en caso contrario retorna falso"""
        super(TeamMemberFormSet,self).is_valid()
        self.vacio = False
        self.sin_usuario = False
        self.sin_rol = False
        self.doble_usuario = False
        if not self.forms:
            self.vacio = True
            return False
        all_delete = True
        usuarios = []
        roles = []
        for form in self.forms:
            # verificacion de roles unicos
            if form['rol'].value():
                rol = Rol.objects.get(pk=form['rol'].value())
                if rol.is_unique and form['rol'].value() in roles:
                    self.rol_doble = rol
                    return False
                if not form['rol'].value() in roles:
                    roles.append(form['rol'].value())

            # un usuario solo puede asignarse una vez
            if form['usuario'].value() and not form['usuario'].value() in usuarios:
                usuarios.append(form['usuario'].value())
            elif form['usuario'].value() and form['usuario'].value() in usuarios:
                if not form['DELETE'].value():
                    self.doble_usuario = Usuario.objects.get(pk=form['usuario'].value()).username
                    return False
            #existe al menos un form que no se elimina, por lo tanto el formset no esta vacio
            if not form['DELETE'].value():
                all_delete = False
            #todos los forms deben tener usuario
            if not form['usuario'].value() and not form['DELETE'].value():
                self.sin_usuario = True
                return False
            # todos los forms deben tener rol
            if not form['rol'].value() and not form['DELETE'].value():
                self.sin_rol = True
                return False
        #si todos los forms se van a eliminar
        if all_delete:
            self.vacio=True
            return False
        return True
