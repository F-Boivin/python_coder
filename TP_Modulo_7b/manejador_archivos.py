"""Módulo para lectura y escritura segura de archivos de texto.

Provee funciones para leer y escribir archivos usando la sentencia 'with',
garantizando el cierre automático del archivo y el uso de codificación UTF-8.
"""

def leer_datos(ruta):
    """Lee todas las líneas de un archivo de texto.

    Args:
        ruta (str | Path): Ruta del archivo a leer.

    Returns:
        list[str]: Lista con las líneas del archivo (incluye el salto de línea).

    Raises:
        FileNotFoundError: Si el archivo no existe en la ruta indicada.
        UnicodeDecodeError: Si el archivo no puede decodificarse como UTF-8.
    """
    with open(ruta, 'r', encoding='utf-8') as f:
        return f.readlines()


def escribir_datos(ruta, lista_lineas):
    """Escribe una lista de líneas en un archivo de texto.

    Args:
        ruta (str | Path): Ruta del archivo donde escribir.
        lista_lineas (list[str]): Líneas a escribir. Cada elemento debe
            terminar en '\\n' si se desea separar en líneas.

    Returns:
        None
    """
    with open(ruta, 'w', encoding='utf-8') as f:
        f.writelines(lista_lineas)
