"""
ASGI config for Skyniya Growth OS.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skyniya.settings.development')
application = get_asgi_application()
