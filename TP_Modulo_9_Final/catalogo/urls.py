"""URLs del catálogo: rutas para Libro y Autor."""

from django.urls import path

from .views import (
    AutorCreateView,
    AutorDeleteView,
    AutorDetailView,
    AutorListView,
    AutorUpdateView,
    LibroCreateView,
    LibroDeleteView,
    LibroDetailView,
    LibroListView,
    LibroUpdateView,
)


urlpatterns = [
    # Libros
    path("", LibroListView.as_view(), name="libro-list"),
    path("libros/", LibroListView.as_view(), name="libro-list-alias"),
    path("libros/nuevo/", LibroCreateView.as_view(), name="libro-create"),
    path("libros/<int:pk>/", LibroDetailView.as_view(), name="libro-detail"),
    path("libros/<int:pk>/editar/", LibroUpdateView.as_view(), name="libro-update"),
    path("libros/<int:pk>/eliminar/", LibroDeleteView.as_view(), name="libro-delete"),
    # Autores
    path("autores/", AutorListView.as_view(), name="autor-list"),
    path("autores/nuevo/", AutorCreateView.as_view(), name="autor-create"),
    path("autores/<int:pk>/", AutorDetailView.as_view(), name="autor-detail"),
    path("autores/<int:pk>/editar/", AutorUpdateView.as_view(), name="autor-update"),
    path("autores/<int:pk>/eliminar/", AutorDeleteView.as_view(), name="autor-delete"),
]
