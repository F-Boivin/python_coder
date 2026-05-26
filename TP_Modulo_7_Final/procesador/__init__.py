"""Paquete procesador: lectura, procesamiento y escritura de registros.

Este paquete agrupa los módulos del mini-proyecto del TP final del Módulo 7:

- lectura: funciones para leer datos desde archivos JSON o CSV.
- escritura: funciones para persistir datos procesados en JSON o CSV.
- procesamiento: lógica de negocio (totales y rankings por producto).

Al exponer las funciones públicas vía __init__.py se simplifica la
importación desde main.py (from procesador import leer_csv, ...).
"""

from .lectura import leer_json, leer_csv, parse_fechas
from .escritura import escribir_json, escribir_csv
from .procesamiento import calcular_totales_por_producto, top_n_productos

__all__ = [
    "leer_json",
    "leer_csv",
    "parse_fechas",
    "escribir_json",
    "escribir_csv",
    "calcular_totales_por_producto",
    "top_n_productos",
]
