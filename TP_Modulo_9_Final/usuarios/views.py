"""Vistas de autenticación: solo el registro es custom.

Login y logout se delegan a las vistas built-in de Django configuradas
en usuarios/urls.py.
"""

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import RegistroForm


class RegistroView(CreateView):
    """Registro de nuevo usuario. Tras el alta, redirige al login."""

    form_class = RegistroForm
    template_name = "usuarios/registro.html"
    success_url = reverse_lazy("login")
