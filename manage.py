#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

"""La mayor prueba de si anda los comentarios o no"""


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
#sos una mierda django