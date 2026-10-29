"""Root URLconf: admin, HTML pages and the versioned REST API."""

from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("marketplace.api_urls")),
    path("api/v1/auth/token/", obtain_auth_token, name="api-token"),
    path("", include("marketplace.urls")),
]
