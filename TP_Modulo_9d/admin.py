"""Configuración personalizada del panel admin para el modelo Producto.

Incorpora las tres personalizaciones que pide la consigna (list_display,
search_fields, list_filter) más algunas opciones adicionales que mejoran
significativamente la experiencia de administración: ordering,
list_per_page, list_editable y readonly_fields.
"""

from django.contrib import admin

from .models import Producto


class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "precio", "stock", "disponible")
    search_fields = ("nombre", "descripcion")
    list_filter = ("categoria", "disponible")
    ordering = ("nombre",)
    list_per_page = 25
    list_editable = ("precio", "stock", "disponible")
    readonly_fields = ("creado_en",)


admin.site.register(Producto, ProductoAdmin)
