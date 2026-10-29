"""WSGI entry point for servers such as gunicorn: `gunicorn hub_site.wsgi`."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hub_site.settings")
application = get_wsgi_application()
