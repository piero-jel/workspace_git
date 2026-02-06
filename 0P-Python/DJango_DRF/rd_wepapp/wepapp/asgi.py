"""
ASGI config for wepapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application # type: ignore pylint: disable=import-error

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wepapp.settings')

application = get_asgi_application()
