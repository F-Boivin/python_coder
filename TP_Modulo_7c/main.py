"""Script principal del TP del Módulo 7c.

Demuestra el uso del módulo json para:
  1. Definir un diccionario de configuración de usuario.
  2. Guardarlo en disco con json.dump (envuelto en manejador_json.guardar_json).
  3. Cargarlo de vuelta con json.load y verificar que coincide.
  4. Manejar tipos no serializables (datetime) con el parámetro default.
"""

import json
from datetime import datetime
from pathlib import Path

import manejador_json as mj

# Ruta del archivo de configuración (portable entre SO con pathlib)
BASE_DIR = Path(__file__).parent
ruta_config = BASE_DIR / "config_usuario.json"

# --- 1. Diccionario de preferencias del usuario ---
# Incluye un datetime para demostrar el manejo de tipos no serializables.
configuracion = {
    "usuario": "felipe",
    "tema": "oscuro",
    "idioma": "es-AR",
    "volumen": 75,
    "notificaciones": True,
    "ultimo_acceso": datetime.now(),
}

print("Configuración original (en memoria):")
for clave, valor in configuracion.items():
    print(f"  {clave}: {valor!r}")
print()

# --- 2. Guardar en JSON ---
try:
    mj.guardar_json(ruta_config, configuracion)
    print(f"Archivo '{ruta_config.name}' guardado correctamente.\n")
except TypeError as e:
    print(f"Error de serialización: {e}")
except PermissionError:
    print(f"Error: no hay permisos para escribir en '{ruta_config}'.")

# --- 3. Cargar el archivo de vuelta ---
try:
    config_cargada = mj.cargar_json(ruta_config)
    print("Configuración cargada desde el archivo:")
    for clave, valor in config_cargada.items():
        print(f"  {clave}: {valor!r}")
    print()
except FileNotFoundError:
    print(f"Error: '{ruta_config}' no fue encontrado.")
except json.JSONDecodeError as e:
    print(f"Error: el archivo no contiene JSON válido — {e}")

# --- 4. Verificación de integridad ---
# El datetime original se convirtió a string ISO al serializar,
# por eso la comparación directa no es exacta. Convertimos para comparar.
original_normalizado = {
    **configuracion,
    "ultimo_acceso": configuracion["ultimo_acceso"].isoformat(),
}
if config_cargada == original_normalizado:
    print("Verificación: el contenido cargado coincide con el original.")
else:
    print("Verificación: hay diferencias entre el original y lo cargado.")
