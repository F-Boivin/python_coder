"""URLs raíz del proyecto workshop.

Delega todas las rutas de la app core usando include() con namespacing
(app_name = 'core' definido en core/urls.py). Este es el patrón de URLs
avanzadas de la Unidad 7.
"""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
]
