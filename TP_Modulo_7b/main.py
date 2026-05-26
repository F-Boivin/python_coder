"""Script principal del TP del Módulo 7b.

Lee el archivo datos.txt usando el módulo manejador_archivos, muestra su
contenido por consola y luego genera un archivo salida.txt con nuevas líneas.
Maneja errores comunes: archivo inexistente y problemas de codificación.
"""

from pathlib import Path
import manejador_archivos as ma

# Construcción de rutas con pathlib (portable entre sistemas operativos)
BASE_DIR = Path(__file__).parent
ruta_datos = BASE_DIR / "datos.txt"
ruta_salida = BASE_DIR / "salida.txt"

# --- Lectura del archivo datos.txt con manejo de errores ---
try:
    lineas = ma.leer_datos(ruta_datos)
    print("Contenido de datos.txt:")
    print("-" * 40)
    for numero, linea in enumerate(lineas, start=1):
        print(f"Línea {numero}: {linea.rstrip()}")
    print("-" * 40)
except FileNotFoundError:
    print(f"Error: el archivo '{ruta_datos}' no fue encontrado.")
except UnicodeDecodeError:
    print(f"Error: no se pudo decodificar '{ruta_datos}' como UTF-8.")
except PermissionError:
    print(f"Error: no hay permisos para leer '{ruta_datos}'.")

# --- Escritura del archivo salida.txt ---
nuevas_lineas = [
    "Esta es la primera línea generada por el script.\n",
    "Segunda línea escrita con escribir_datos().\n",
    "Tercera línea para verificar writelines().\n",
    "Archivo creado correctamente con UTF-8.\n",
]

try:
    ma.escribir_datos(ruta_salida, nuevas_lineas)
    print(f"\nArchivo '{ruta_salida.name}' creado correctamente.")
except PermissionError:
    print(f"Error: no hay permisos para escribir en '{ruta_salida}'.")
