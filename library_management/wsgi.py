"""
WSGI config for library_management project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_management.settings')
django.setup()

# Auto-migrate on startup (temporary, only for deployment)
from django.core.management import call_command
call_command('migrate', interactive=False)
call_command('collectstatic', interactive=False, verbosity=0)

application = get_wsgi_application()