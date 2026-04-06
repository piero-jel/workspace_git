"""
WSGI config for ticketsys project.

It exposes the WSGI callable as a module-level variable named `application`.
"""
# buil-in import
import os

# framework import
from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

## gunicorn config.wsgi:application
application = get_wsgi_application()
