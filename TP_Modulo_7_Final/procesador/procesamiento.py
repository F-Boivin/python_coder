"""Lógica de procesamiento de registros de ventas.

Funciones puras (sin I/O) que toman registros ya leídos y calculan
métricas agregadas. Mantener el procesamiento separado de la lectura
y escritura facilita las pruebas unitarias y la reutilización.
"""

from collections import defaultdict


def calcular_totales_por_producto(registros):
    """Calcula el total facturado por cada producto.

    Recorre la lista de registros, multiplica cantidad por precio
    unitario y suma por producto. Convierte explícitamente los valores
    a int/float porque al leer un CSV todos los campos llegan como
    strings.

    Args:
        registros (list[dict]): Lista de registros, cada uno con claves
            'producto', 'cantidad' y 'precio_unitario'.

    Returns:
        dict[str, float]: Diccionario {producto: total_facturado}.

    Raises:
        KeyError: Si algún registro no tiene las claves requeridas.
        ValueError: Si cantidad o precio_unitario no son numéricos.
    """
    totales = defaultdict(float)
    for r in registros:
        producto = r["producto"]
        cantidad = int(r["cantidad"])
        precio = float(r["precio_unitario"])
        totales[producto] += cantidad * precio
    return dict(totales)


def top_n_productos(totales, n=3):
    """Devuelve los N productos con mayor facturación.

    Args:
        totales (dict[str, float]): Diccionario {producto: total}.
        n (int): Cantidad de productos a devolver. Por defecto 3.

    Returns:
        list[tuple[str, float]]: Lista de tuplas (producto, total)
            ordenadas de mayor a menor por total. Tiene como máximo n
            elementos.
    """
    return sorted(totales.items(), key=lambda x: x[1], reverse=True)[:n]
