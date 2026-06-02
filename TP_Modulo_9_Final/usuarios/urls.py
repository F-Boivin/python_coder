"""URLs de autenticación.

Usa LoginView y LogoutView built-in de Django y delega solo el registro
a una vista custom (RegistroView).
"""

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import RegistroView


urlpatterns = [
    path(
        "login/",
        LoginView.as_view(template_name="usuarios/login.html"),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
    path(
        "registro/",
        RegistroView.as_view(),
        name="registro",
    ),
]
