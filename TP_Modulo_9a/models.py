"""Modelo Producto para el TP del Módulo 9 — Unidad 3.

Definido por la consigna del curso. Representa un producto básico con
nombre, descripción y precio, persistido en SQLite vía el ORM de Django.
"""

from django.db import models


class Producto(models.Model):
    """Producto comercializable con datos mínimos para un catálogo.

    Atributos:
        nombre: Nombre del producto, texto corto (hasta 100 caracteres).
        descripcion: Descripción extendida, opcional.
        precio: Precio unitario con dos decimales, hasta 8 dígitos en total
            (es decir, valores hasta 999.999,99).
    """

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.nombre
