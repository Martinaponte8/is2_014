"""
WSGI config for is2_014 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
# configuramos el runserver django para poder correr la aplicacion

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'is2_014.settings')

application = get_wsgi_application()
