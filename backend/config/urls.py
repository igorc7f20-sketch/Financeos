"""
Root URL configuration.
Each app registers its own urls — this file only aggregates them.
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerUIView

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # API v1
    path("api/auth/", include("apps.users.urls")),
    # Swagger / OpenAPI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerUIView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
