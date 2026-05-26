"""Funciones para leer registros desde archivos JSON o CSV.

Todas las funciones de este módulo usan la sentencia 'with' para
garantizar el cierre del archivo, codificación UTF-8 explícita y
manejan los parámetros recomendados (newline='' para CSV).
"""

import csv
import json
from datetime import datetime


def leer_json(ruta, object_hook=None):
    """Lee un archivo JSON y devuelve el objeto Python resultante.

    Args:
        ruta (str | Path): Ruta del archivo JSON a leer.
        object_hook (callable | None): Callback opcional que se aplica a
            cada diccionario decodificado. Útil para reconstruir tipos
            como datetime (ver parse_fechas).

    Returns:
        El objeto Python decodificado (típicamente dict o list).

    Raises:
        FileNotFoundError: Si el archivo no existe.
        json.JSONDecodeError: Si el contenido no es JSON válido.
        UnicodeDecodeError: Si la codificación no es UTF-8.
    """
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f, object_hook=object_hook)


def parse_fechas(dct):
    """object_hook para json.load que convierte strings ISO 8601 a datetime.

    Recorre cada par clave-valor del diccionario y, si el valor parece
    una fecha ISO, lo convierte al tipo datetime. Esta función es la
    contraparte del callback default usado al serializar (ver escritura).

    Args:
        dct (dict): Diccionario decodificado por json.load.

    Returns:
        dict: El mismo diccionario con strings de fecha convertidos.
    """
    for clave, valor in dct.items():
        if isinstance(valor, str) and len(valor) >= 10:
            try:
                dct[clave] = datetime.fromisoformat(valor)
            except ValueError:
                pass  # No era una fecha, lo dejamos como string
    return dct


def leer_csv(ruta, delimitador=","):
    """Lee un archivo CSV con cabeceras y devuelve una lista de dicts.

    Usa csv.DictReader, que asigna cada fila a un dict cuyas claves son
    los nombres de columna definidos en la primera fila. Si una fila
    tiene menos columnas, las faltantes quedan en None.

    Args:
        ruta (str | Path): Ruta del archivo CSV.
        delimitador (str): Separador de campos. Por defecto ','.

    Returns:
        list[dict]: Filas del archivo como diccionarios.

    Raises:
        FileNotFoundError: Si el archivo no existe.
        UnicodeDecodeError: Si la codificación no es UTF-8.
    """
    # newline='' es indispensable en CSV para evitar problemas de saltos
    # de línea en Windows (\r\n vs \n).
    with open(ruta, "r", newline="", encoding="utf-8") as f:
        lector = csv.DictReader(f, delimiter=delimitador)
        return list(lector)
