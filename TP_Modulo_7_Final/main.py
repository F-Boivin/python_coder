"""Script principal del TP final del Módulo 7.

Herramienta de procesamiento de registros de ventas:
  1. Lee un CSV con ventas (csv.DictReader).
  2. Calcula totales facturados por producto y top-3.
  3. Persiste el reporte completo en JSON y un resumen tabular en CSV.

Sigue la consigna de la Unidad 8 del Módulo 7: paquete propio (procesador),
script principal con if __name__ == "__main__", uso consistente de with,
manejo de errores y mensajes claros de inicio/proceso/finalización.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

from procesador import (
    leer_csv,
    escribir_json,
    escribir_csv,
    calcular_totales_por_producto,
    top_n_productos,
)

# --- Configuración de rutas (portable con pathlib) ---
BASE_DIR = Path(__file__).parent
RUTA_ENTRADA = BASE_DIR / "datos" / "ventas.csv"
RUTA_REPORTE_JSON = BASE_DIR / "reporte.json"
RUTA_REPORTE_CSV = BASE_DIR / "reporte.csv"


def imprimir_separador(titulo=""):
    """Imprime una línea de separación visual en consola."""
    print("=" * 60)
    if titulo:
        print(titulo)
        print("=" * 60)


def main():
    """Función principal: orquesta lectura, procesamiento y escritura."""
    imprimir_separador("Iniciando procesamiento de registros de ventas...")

    # --- 1. Lectura del CSV de entrada ---
    try:
        registros = leer_csv(RUTA_ENTRADA)
        print(f"[OK] {len(registros)} registros leídos desde '{RUTA_ENTRADA.name}'.")
    except FileNotFoundError:
        print(f"[ERROR] No se encontró el archivo de entrada: {RUTA_ENTRADA}")
        sys.exit(1)
    except PermissionError:
        print(f"[ERROR] Sin permisos para leer: {RUTA_ENTRADA}")
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"[ERROR] No se pudo decodificar el archivo como UTF-8: {RUTA_ENTRADA}")
        sys.exit(1)

    # --- 2. Procesamiento ---
    print("[..] Calculando totales por producto...")
    try:
        totales = calcular_totales_por_producto(registros)
        top3 = top_n_productos(totales, n=3)
        print(f"[OK] {len(totales)} productos distintos procesados.")
    except (KeyError, ValueError) as e:
        print(f"[ERROR] Datos inválidos en el CSV: {e}")
        sys.exit(1)

    # --- 3. Construcción del reporte ---
    reporte = {
        "generado_en": datetime.now(),
        "archivo_origen": RUTA_ENTRADA.name,
        "total_registros": len(registros),
        "total_facturado": round(sum(totales.values()), 2),
        "totales_por_producto": {
            prod: round(total, 2) for prod, total in totales.items()
        },
        "top_3_productos": [
            {"producto": prod, "total_facturado": round(total, 2)}
            for prod, total in top3
        ],
    }

    # --- 4. Escritura del reporte (JSON detallado + CSV tabular) ---
    try:
        escribir_json(RUTA_REPORTE_JSON, reporte)
        print(f"[OK] Reporte JSON guardado en '{RUTA_REPORTE_JSON.name}'.")

        filas_csv = [
            {"producto": prod, "total_facturado": round(total, 2)}
            for prod, total in sorted(totales.items(), key=lambda x: x[1], reverse=True)
        ]
        escribir_csv(
            RUTA_REPORTE_CSV,
            filas_csv,
            campos=["producto", "total_facturado"],
        )
        print(f"[OK] Reporte CSV guardado en '{RUTA_REPORTE_CSV.name}'.")
    except (PermissionError, OSError) as e:
        print(f"[ERROR] No se pudo escribir el reporte: {e}")
        sys.exit(1)

    # --- 5. Resumen en consola ---
    print()
    imprimir_separador("Resumen del procesamiento")
    print(f"Registros procesados:    {reporte['total_registros']}")
    print(f"Productos distintos:     {len(totales)}")
    print(f"Total facturado:         ${reporte['total_facturado']:,.2f}")
    print()
    print("Top 3 productos:")
    for posicion, (producto, total) in enumerate(top3, start=1):
        print(f"  {posicion}. {producto:<15} ${total:,.2f}")
    print()
    imprimir_separador("Procesamiento finalizado correctamente.")


def demo_lectura_inversa():
    """Demo opcional: lee el reporte.json reconstruyendo el datetime.

    Demuestra el uso del parámetro object_hook de json.load para
    convertir strings ISO 8601 de vuelta a objetos datetime, cerrando
    el ciclo de la serialización asimétrica.
    """
    from procesador import leer_json, parse_fechas

    if not RUTA_REPORTE_JSON.exists():
        return

    print("\n[Demo extra] Releyendo reporte.json con object_hook:")
    try:
        reporte = leer_json(RUTA_REPORTE_JSON, object_hook=parse_fechas)
        gen = reporte["generado_en"]
        print(f"  Tipo de 'generado_en': {type(gen).__name__}")
        print(f"  Valor: {gen}")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"  [WARN] No se pudo releer el reporte: {e}")


# --- Patrón __name__ == "__main__" ---
# Esto asegura que main() solo se ejecute cuando el archivo se corre
# directamente. Si alguien importa este script como módulo (ej. para
# reutilizar funciones), el código no se dispara automáticamente.
if __name__ == "__main__":
    main()
    demo_lectura_inversa()
