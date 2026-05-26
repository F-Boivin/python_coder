"""Funciones para guardar datos procesados en archivos JSON o CSV.

Todas las funciones abren los archivos con 'with', usan UTF-8 y aplican
los parámetros recomendados (ensure_ascii=False e indent en JSON,
newline='' en CSV).
"""

import csv
import json
from datetime import datetime


def _serializar_extras(obj):
    """Callback default para json.dump: convierte tipos no serializables.

    Args:
        obj: Objeto que json no sabe serializar nativamente.

    Returns:
        Representación serializable del objeto.

    Raises:
        TypeError: Si el tipo no está contemplado.
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Tipo no serializable: {type(obj).__name__}")


def escribir_json(ruta, datos):
    """Serializa un objeto Python y lo guarda en un archivo JSON.

    Aplica ensure_ascii=False para preservar tildes y ñ legibles, e
    indent=4 para formato amigable. El callback default permite
    serializar datetime sin error.

    Args:
        ruta (str | Path): Ruta del archivo destino.
        datos: Objeto Python a serializar.

    Raises:
        TypeError: Si datos contiene un tipo no soportado.
        PermissionError: Si no hay permisos de escritura.
    """
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(
            datos,
            f,
            ensure_ascii=False,
            indent=4,
            default=_serializar_extras,
        )


def escribir_csv(ruta, filas, campos, delimitador=","):
    """Guarda una lista de diccionarios en un archivo CSV con cabeceras.

    Usa csv.DictWriter, que toma fieldnames como definición de columnas
    y escribe automáticamente la fila de cabecera.

    Args:
        ruta (str | Path): Ruta del archivo destino.
        filas (list[dict]): Filas a escribir; cada dict debe tener las
            claves indicadas en `campos`.
        campos (list[str]): Nombres de columna en el orden deseado.
        delimitador (str): Separador de campos. Por defecto ','.

    Raises:
        PermissionError: Si no hay permisos de escritura.
        ValueError: Si una fila tiene una clave no declarada en campos.
    """
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=campos, delimiter=delimitador)
        escritor.writeheader()
        escritor.writerows(filas)
