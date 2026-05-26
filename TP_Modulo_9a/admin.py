"""Registro del modelo Producto en el panel de administración de Django.

Al llamar a admin.site.register(Producto), Django agrega el modelo al
AdminSite por defecto. Esto activa la generación automática de las vistas
de listado, creación, edición y eliminación de instancias del modelo bajo
la URL /admin, sin necesidad de escribir formularios ni templates.
"""

from django.contrib import admin

from .models import Producto

admin.site.register(Producto)
