"""Formulario de registro de usuarios."""

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegistroForm(UserCreationForm):
    """Extiende UserCreationForm agregando email obligatorio."""

    email = forms.EmailField(required=True, help_text="Necesario para recuperar la cuenta.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
