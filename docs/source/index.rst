.. Gestor de Proyectos documentation master file, created by
   sphinx-quickstart on Mon Aug 16 10:42:55 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Gestor de Proyectos's documentation!
===============================================
.. include:: ../../README.rst
   :start-after: My Project Header
   :end-before: My second header

############
My Functions
############

Estas son las funciones que proporciona nuestro proyecto

.. toctree::
   :maxdepth: 2
   :caption: Contents:

############
Settings.py 12/08/2021
############

#se importa la libreria path

from pathlib import Path

# se indica la direccion base del path

BASE_DIR = Path(__file__).resolve().parent.parent


# ADVERTENCIA DE SEGURIDAD: mantenga la clave secreta utilizada en producción en secreto!

SECRET_KEY = 'django-insecure-#%-!0%=56hnp7+4f1wy1ucxx**)-2-uvz)mb=tbf$#ga8==4+-'

# ADVERTENCIA DE SEGURIDAD: no ejecute con la depuración activada en producción!

DEBUG = True

ALLOWED_HOSTS = []


# Definicion de las aplicaciones instaladas

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.sites',
    'is2_014_app',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'is2_014.urls'

#Plantillas

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'is2_014.wsgi.application'

#definimos la base de datos y la configuramos

DATABASES = {
    'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sistemagestor',
        'USER': 'postgres',
        'PASSWORD':'postgres',
        'HOST':'localhost',
        'PORT': '5432',
    }
}

# validacion de contraseñas

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

#para importar la imagen del inicio de sesion

STATIC_URL = '/static/'


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#configuramos django como backend de autentificacion

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]

#para los proveedores de cuentas sociales configuramos a google

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

#se agrega un sitio ID y se redirije a los usuarios a una ruta base despues del inicio de sesion

SITE_ID = 2

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

############
Urls.py 13/08/2021
############

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

# configuramos las rutas y vistas

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="index.html")),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view()),
]

############
Wsgi.py 13/08/2021
############

import os

from django.core.wsgi import get_wsgi_application
# configuramos el runserver django para poder correr la aplicacion

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'is2_014.settings')

application = get_wsgi_application()

############
Index.html 15/08/2021
############

{% load socialaccount %}
{% load static %}
<html>
<body>

<!--Titulo de la pagina-->

<h1><center>Gestor de proyectos </center></h1>

<!--Codigo para agregar la imagen a la pagina, pasandole el directorio donde se encuentra la foto estatica -->

<br> <center><img alt="My image" src="{% static 'is2_014_app/logo.png' %}"></center>

<!--Funcion de python para autenticar el inicio de sesion de un usuario -->

{% if user.is_authenticated %}



 <center> <p>Bienvenido, Te has logueado como {{ user.username }}</p></center>
<br> <center><a href="logout">Cerrar sesion</a></center>


 <!--<li><a href="../accounts/logout/"><span class="glyphicon glyphicon-log-out"></span> Cerrar Sesión</a></li>

Si no esta logueado mostrarle la pagina de inicio con el link para loguearse con google -->

{% else %}
 <br> <center><a href="{% provider_login_url 'google' %}">Logueate con Google</a></center>
{% endif %}
</body>
</html>

############
Manage.py 15/08/2021
############

import os
import sys

# corremos el servidor y lanzamos errores en caso de no poder conectarse

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'is2_014.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()