"""Modelos del blog: Author, Tag y Post.

Implementa el dominio pedido en la Unidad 3 del Módulo 10:
- Author: name, email (único).
- Tag: name.
- Post: title, content, published_date, FK a Author, M2M a Tag,
  ordenado por fecha descendente, con validación personalizada en clean().
"""

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class Author(models.Model):
    """Autor de publicaciones del blog."""

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "autor"
        verbose_name_plural = "autores"

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Etiqueta para clasificar publicaciones."""

    name = models.CharField(max_length=30)

    class Meta:
        ordering = ["name"]
        verbose_name = "etiqueta"
        verbose_name_plural = "etiquetas"

    def __str__(self):
        return self.name


class Post(models.Model):
    """Publicación del blog.

    Relaciones:
        - author: FK a Author (un autor escribe muchos posts).
        - tags: M2M a Tag (un post tiene muchas etiquetas y viceversa).
    """

    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")

    class Meta:
        ordering = ["-published_date"]
        verbose_name = "publicación"
        verbose_name_plural = "publicaciones"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:post-detail", kwargs={"pk": self.pk})

    def clean(self):
        """Validación personalizada: el título debe tener al menos 5 caracteres."""
        if len(self.title.strip()) < 5:
            raise ValidationError(
                {"title": "El título debe tener al menos 5 caracteres."}
            )
