from django.urls import path

from .views import LibroCreateView, LibroUpdateView


urlpatterns = [
    path('libro/nuevo/', LibroCreateView.as_view(), name='libro-create'),
    path('libro/<int:pk>/editar/', LibroUpdateView.as_view(), name='libro-update'),
]
