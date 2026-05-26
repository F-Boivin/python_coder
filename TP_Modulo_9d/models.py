"""Modelo Producto enriquecido para demostrar las opciones de ModelAdmin.

Incluye los campos sugeridos por la consigna (nombre, descripcion, precio,
stock, categoria, disponible) que permiten ejercitar las tres
personalizaciones clave: list_display, search_fields y list_filter.
"""

from django.db import models


class Producto(models.Model):
    """Producto de un catálogo de tienda online.

    Campos elegidos para que cada uno tenga un rol claro en el admin:
        - nombre / descripcion: candidatos a `search_fields` (búsqueda).
        - precio / stock: candidatos a `list_display` (columnas).
        - categoria / disponible: candidatos a `list_filter` (sidebar).
    """

    CATEGORIA_CHOICES = [
        ("libros", "Libros"),
        ("tecnologia", "Tecnología"),
        ("hogar", "Hogar"),
        ("ropa", "Ropa"),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    disponible = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "producto"
        verbose_name_plural = "productos"

    def __str__(self):
        return self.nombre
