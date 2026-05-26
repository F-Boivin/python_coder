# TP Módulo 7b — Manejo de archivos y persistencia de datos

Trabajo práctico de la Unidad 4 del Módulo 7 del curso de Python de Coderhouse.

## Consigna

Crear un módulo propio `manejador_archivos` con funciones para leer y escribir archivos de texto usando `with`, `pathlib` y manejo de excepciones, y consumirlo desde un script principal.

Requisitos:
- Función `leer_datos(ruta)` que lea todas las líneas con `readlines()`.
- Función `escribir_datos(ruta, lista_lineas)` que escriba una lista de líneas con `writelines()`.
- Manejo de `FileNotFoundError` y errores de encoding con `try-except`.
- Uso de `pathlib` para construir rutas portables.
- Codificación `utf-8` en todas las operaciones de archivo.

## Estructura

```
TP_Modulo_7b/
├── datos.txt                 # Archivo de entrada con 5 líneas de prueba
├── manejador_archivos.py     # Módulo propio (leer_datos, escribir_datos)
├── main.py                   # Script principal
└── salida.txt                # Generado al ejecutar main.py
```

## Cómo ejecutar

```bash
python main.py
```

**En Windows**, si la consola muestra mal las tildes y ñ, activá UTF-8 antes:

```powershell
chcp 65001
python main.py
```

## Salida esperada

```
Contenido de datos.txt:
----------------------------------------
Línea 1: Primera línea del archivo de datos.
Línea 2: Segunda línea con información de ejemplo.
Línea 3: Tercera línea para probar la lectura.
Línea 4: Cuarta línea con caracteres especiales: áéíóú ñ.
Línea 5: Quinta y última línea del archivo.
----------------------------------------

Archivo 'salida.txt' creado correctamente.
```

## Conceptos aplicados

- `with open(...)` para cierre automático de archivos.
- `encoding='utf-8'` en todas las operaciones de I/O.
- `pathlib.Path` para rutas portables entre sistemas operativos.
- Captura específica de excepciones: `FileNotFoundError`, `UnicodeDecodeError`, `PermissionError`.
- Importación de módulo propio con alias (`import manejador_archivos as ma`).
- Docstrings PEP 257 con secciones `Args`, `Returns` y `Raises`.

## Entrega

- **Google Doc:** https://docs.google.com/document/d/1yZusMRv6AE2wehyIVLz0d3ecQjavNJwrHzZcnLzjJnM/edit?usp=sharing
- **Nota recibida:** _pendiente_
