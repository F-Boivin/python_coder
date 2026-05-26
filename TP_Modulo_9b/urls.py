from django.urls import path

from .views import LibroListView, LibroDetailView


urlpatterns = [
    path('libros/', LibroListView.as_view(), name='lista_libros'),
    path('libros/<int:pk>/', LibroDetailView.as_view(), name='detalle_libro'),
]
