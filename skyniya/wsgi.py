
"""
WSGI config for Skyniya Growth OS.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'skyniya.settings.production'
)

application = get_wsgi_application()
