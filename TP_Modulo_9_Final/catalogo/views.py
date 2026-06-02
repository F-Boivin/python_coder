"""Vistas CRUD para Autor y Libro usando Class-Based Views.

Estructura de permisos:
- List y Detail: público (cualquiera puede ver el catálogo).
- Create:        requiere login (LoginRequiredMixin).
- Update/Delete: requiere login + ser el creador del libro
                 (LoginRequiredMixin + UserPassesTestMixin).
"""

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import AutorForm, LibroForm
from .models import Autor, Libro


# ---------------------------------------------------------------------------
# Vistas para Libro
# ---------------------------------------------------------------------------

class LibroListView(ListView):
    """Listado público de libros con paginación.

    Usa select_related('autor') para evitar el problema N+1: en una sola
    query trae los libros y sus autores asociados, en lugar de hacer una
    query por libro al renderizar `{{ libro.autor }}` en el template.
    """

    model = Libro
    template_name = "catalogo/libro_list.html"
    context_object_name = "libros"
    paginate_by = 10

    def get_queryset(self):
        return Libro.objects.select_related("autor").all()


class LibroDetailView(DetailView):
    model = Libro
    template_name = "catalogo/libro_detail.html"
    context_object_name = "libro"

    def get_queryset(self):
        return Libro.objects.select_related("autor", "creado_por")


class LibroCreateView(LoginRequiredMixin, CreateView):
    """Crear un libro. Requiere login.

    Sobreescribe form_valid para asignar automáticamente el usuario actual
    como creador del libro (patrón típico en sistemas multi-usuario).
    """

    model = Libro
    form_class = LibroForm
    template_name = "catalogo/libro_form.html"
    success_url = reverse_lazy("libro-list")

    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        return super().form_valid(form)


class LibroUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Editar un libro. Solo el creador puede hacerlo."""

    model = Libro
    form_class = LibroForm
    template_name = "catalogo/libro_form.html"
    success_url = reverse_lazy("libro-list")

    def test_func(self):
        """UserPassesTestMixin: el usuario actual debe ser el creador."""
        libro = self.get_object()
        return self.request.user == libro.creado_por


class LibroDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Eliminar un libro. Solo el creador puede hacerlo."""

    model = Libro
    template_name = "catalogo/libro_confirm_delete.html"
    success_url = reverse_lazy("libro-list")
    context_object_name = "libro"

    def test_func(self):
        libro = self.get_object()
        return self.request.user == libro.creado_por


# ---------------------------------------------------------------------------
# Vistas para Autor
# ---------------------------------------------------------------------------

class AutorListView(ListView):
    model = Autor
    template_name = "catalogo/autor_list.html"
    context_object_name = "autores"
    paginate_by = 20


class AutorDetailView(DetailView):
    """Detalle de un autor; incluye los libros asociados.

    Usa prefetch_related para traer los libros del autor en una sola query
    adicional (evita N+1 al iterar `autor.libros.all` en el template).
    """

    model = Autor
    template_name = "catalogo/autor_detail.html"
    context_object_name = "autor"

    def get_queryset(self):
        return Autor.objects.prefetch_related("libros")


class AutorCreateView(LoginRequiredMixin, CreateView):
    model = Autor
    form_class = AutorForm
    template_name = "catalogo/autor_form.html"
    success_url = reverse_lazy("autor-list")


class AutorUpdateView(LoginRequiredMixin, UpdateView):
    model = Autor
    form_class = AutorForm
    template_name = "catalogo/autor_form.html"
    success_url = reverse_lazy("autor-list")


class AutorDeleteView(LoginRequiredMixin, DeleteView):
    model = Autor
    template_name = "catalogo/autor_confirm_delete.html"
    success_url = reverse_lazy("autor-list")
    context_object_name = "autor"
