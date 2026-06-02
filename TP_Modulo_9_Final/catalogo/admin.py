"""Registro de modelos en el panel admin con configuraciones avanzadas.

Aplica patrones aprendidos en el TP 9d:
- list_display, search_fields, list_filter (los básicos)
- list_select_related (lección del 9d: optimiza queries con FK)
- ordering, list_per_page (UX)
- Admin actions personalizadas (sugerencia del 9d corrector)
"""

from django.contrib import admin

from .models import Autor, Libro


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ("apellido", "nombre", "nacionalidad", "cantidad_libros")
    search_fields = ("apellido", "nombre", "nacionalidad")
    list_filter = ("nacionalidad",)
    ordering = ("apellido", "nombre")

    @admin.display(description="Libros publicados")
    def cantidad_libros(self, obj):
        return obj.libros.count()


@admin.action(description="Marcar como disponibles")
def marcar_disponibles(modeladmin, request, queryset):
    """Acción masiva: marca múltiples libros como disponibles de una sola vez."""
    queryset.update(disponible=True)


@admin.action(description="Marcar como NO disponibles")
def marcar_no_disponibles(modeladmin, request, queryset):
    queryset.update(disponible=False)


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "autor",
        "fecha_publicacion",
        "disponible",
        "creado_por",
    )
    search_fields = ("titulo", "descripcion", "autor__apellido", "autor__nombre")
    list_filter = ("disponible", "fecha_publicacion", "autor")
    ordering = ("titulo",)
    list_per_page = 25
    list_editable = ("disponible",)
    readonly_fields = ("creado_en", "actualizado_en")
    # list_select_related: cuando list_display incluye 'autor' (FK), Django
    # haría una query por cada fila para resolverlo. Con esta opción usa
    # un JOIN y trae todo en una sola query (lección del feedback TP 9d).
    list_select_related = ("autor", "creado_por")
    actions = [marcar_disponibles, marcar_no_disponibles]
