from django.views.generic import ListView, DetailView

from .models import Libro


class LibroListView(ListView):
    model = Libro
    template_name = 'libros/lista_libros.html'
    context_object_name = 'libros'


class LibroDetailView(DetailView):
    model = Libro
    template_name = 'libros/detalle_libro.html'
    context_object_name = 'libro'
