"""Modelos del catálogo: Autor y Libro con relación ForeignKey.

Diseño:
- Autor es un modelo independiente con campos simples.
- Libro tiene un FK a Autor (un libro es escrito por un autor; un autor
  puede haber escrito muchos libros).
- Libro también guarda quién lo creó (FK a User) para habilitar permisos
  por owner en las vistas de edición/borrado.
"""

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


User = get_user_model()


class Autor(models.Model):
    """Autor de uno o más libros."""

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=50, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["apellido", "nombre"]
        verbose_name = "autor"
        verbose_name_plural = "autores"

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

    def get_absolute_url(self):
        """URL canónica para un autor (usada por CreateView/UpdateView)."""
        return reverse("autor-detail", kwargs={"pk": self.pk})


class Libro(models.Model):
    """Libro del catálogo. Relacionado a un Autor (FK) y a un User creador."""

    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(
        Autor,
        on_delete=models.CASCADE,
        related_name="libros",
    )
    fecha_publicacion = models.DateField()
    descripcion = models.TextField(blank=True)
    disponible = models.BooleanField(default=True)
    creado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="libros_creados",
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["titulo"]
        verbose_name = "libro"
        verbose_name_plural = "libros"

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("libro-detail", kwargs={"pk": self.pk})
