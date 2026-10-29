"""ASGI entry point for async servers such as uvicorn: `uvicorn hub_site.asgi:application`."""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hub_site.settings")
application = get_asgi_application()
