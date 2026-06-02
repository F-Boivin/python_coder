"""ModelForms para Autor y Libro.

Se usan en CreateView y UpdateView para validar y persistir los datos
ingresados desde el frontend.
"""

from django import forms

from .models import Autor, Libro


class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ["nombre", "apellido", "nacionalidad", "fecha_nacimiento"]
        widgets = {
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date"}),
        }


class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ["titulo", "autor", "fecha_publicacion", "descripcion", "disponible"]
        widgets = {
            "fecha_publicacion": forms.DateInput(attrs={"type": "date"}),
            "descripcion": forms.Textarea(attrs={"rows": 4}),
        }
