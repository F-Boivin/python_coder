"""URLs de la app core con namespacing (Unidad 7).

app_name habilita el namespace 'core', de modo que las rutas se referencian
como 'core:post-list', 'core:post-detail', etc. en templates y vistas.
Usa converters (<int:pk>) para capturar parámetros de la URL.
"""

from django.urls import path

from . import views


app_name = "core"

urlpatterns = [
    path("", views.PostListView.as_view(), name="post-list"),
    path("posts/nuevo/", views.PostCreateView.as_view(), name="post-create"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("posts/<int:pk>/editar/", views.PostUpdateView.as_view(), name="post-update"),
    path("posts/<int:pk>/eliminar/", views.PostDeleteView.as_view(), name="post-delete"),
]
