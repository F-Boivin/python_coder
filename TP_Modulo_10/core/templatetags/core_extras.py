"""Tags y filtros personalizados de la app core (Unidad 6).

Demuestra cómo extender el lenguaje de templates de Django con lógica
propia, registrada en una librería de templatetags.
"""

from django import template

register = template.Library()


@register.filter(name="mayusculas")
def mayusculas(value):
    """Filtro: convierte un texto a MAYÚSCULAS.

    Uso en template: {{ post.title|mayusculas }}
    """
    return str(value).upper()


@register.filter(name="resumen")
def resumen(value, longitud=80):
    """Filtro con argumento: recorta el texto a `longitud` caracteres.

    Uso en template: {{ post.content|resumen:120 }}
    """
    texto = str(value)
    if len(texto) <= longitud:
        return texto
    return texto[:longitud].rstrip() + "…"
