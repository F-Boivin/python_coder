"""URLs raíz del proyecto biblioteca.

Delega rutas a las apps:
- /admin/    → panel de administración
- /libros/   → CRUD del catálogo (manejado por catalogo.urls)
- /autores/  → CRUD de autores (también en catalogo.urls)
- /          → home redirige al listado de libros
- /usuarios/ → login, logout, registro (usuarios.urls)
"""

from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("catalogo.urls")),
    path("usuarios/", include("usuarios.urls")),
    # Home (/) redirige al listado de libros para tener una página inicial útil
    path("home/", RedirectView.as_view(pattern_name="libro-list", permanent=False)),
]
