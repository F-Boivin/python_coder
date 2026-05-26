"""Módulo para guardar y cargar archivos JSON de forma segura.

Provee funciones que envuelven json.dump y json.load usando la sentencia
'with' para garantizar el cierre del archivo, codificación UTF-8 y soporte
opcional para tipos no serializables (como datetime) mediante un callback
default.
"""

import json
from datetime import datetime


def guardar_json(ruta, datos):
    """Serializa un objeto Python y lo guarda en un archivo JSON.

    Args:
        ruta (str | Path): Ruta del archivo destino.
        datos: Objeto Python a serializar. Tipos soportados nativamente:
            dict, list, str, int, float, bool, None. Los datetime se
            convierten automáticamente a ISO 8601 vía _serializar_extras.

    Returns:
        None

    Raises:
        TypeError: Si datos contiene un tipo no soportado por
            _serializar_extras.
    """
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(
            datos,
            f,
            ensure_ascii=False,  # preserva tildes y ñ legibles en el archivo
            indent=4,            # formato bonito para inspección humana
            default=_serializar_extras,
        )


def cargar_json(ruta):
    """Lee un archivo JSON y lo deserializa a un objeto Python.

    Args:
        ruta (str | Path): Ruta del archivo a leer.

    Returns:
        El objeto Python resultante (típicamente dict o list).

    Raises:
        FileNotFoundError: Si el archivo no existe.
        json.JSONDecodeError: Si el contenido no es JSON válido.
        UnicodeDecodeError: Si el archivo no se puede decodificar como UTF-8.
    """
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)


def _serializar_extras(obj):
    """Convierte objetos no serializables a tipos compatibles con JSON.

    Se pasa como callback al parámetro 'default' de json.dump.

    Args:
        obj: Objeto que json no sabe serializar nativamente.

    Returns:
        Una representación serializable del objeto.

    Raises:
        TypeError: Si el tipo no está contemplado.
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Tipo no serializable: {type(obj).__name__}")
