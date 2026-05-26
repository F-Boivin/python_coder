# TP Módulo 7c — JSON: Datos estructurados

Trabajo práctico de la Unidad 6 del Módulo 7 del curso de Python de Coderhouse.

## Consigna

1. Crear un diccionario Python `configuracion` con al menos tres pares clave-valor que representen preferencias de usuario (ej. tema, idioma, volumen).
2. Usar `json.dump` para guardar ese diccionario en un archivo `config_usuario.json`.
3. Leer el archivo con `json.load` y almacenar el resultado en una variable.
4. Imprimir el contenido cargado para verificar que coincide con el original.
5. (Opcional) Agregar un objeto no serializable (ej. `datetime`) y manejarlo con el parámetro `default`.

Requisitos transversales: usar `with`, codificación `utf-8` y manejo de errores.

## Estructura

```
TP_Modulo_7c/
├── manejador_json.py     # Módulo propio: guardar_json, cargar_json, _serializar_extras
├── main.py               # Script principal
└── config_usuario.json   # Generado al ejecutar main.py
```

## Cómo ejecutar

```bash
python main.py
```

En Windows, si la consola no muestra bien las tildes:

```powershell
chcp 65001
python main.py
```

## Salida esperada

```
Configuración original (en memoria):
  usuario: 'felipe'
  tema: 'oscuro'
  idioma: 'es-AR'
  volumen: 75
  notificaciones: True
  ultimo_acceso: datetime.datetime(2026, 5, 26, 12, 0, 0, 123456)

Archivo 'config_usuario.json' guardado correctamente.

Configuración cargada desde el archivo:
  usuario: 'felipe'
  tema: 'oscuro'
  idioma: 'es-AR'
  volumen: 75
  notificaciones: True
  ultimo_acceso: '2026-05-26T12:00:00.123456'

Verificación: el contenido cargado coincide con el original.
```

> Nota: al cargar el JSON, `ultimo_acceso` aparece como string ISO 8601 en lugar de objeto `datetime`. Eso es esperado: JSON no tiene un tipo nativo de fecha, así que se serializa como texto y se debe parsear con `datetime.fromisoformat()` si se quiere recuperar el tipo original.

## Conceptos aplicados

- `json.dump` / `json.load` para serializar y deserializar objetos Python.
- `ensure_ascii=False` para preservar tildes y ñ legibles en el archivo.
- `indent=4` para formato legible por humanos.
- Parámetro `default` con callback `_serializar_extras` para manejar tipos no nativos de JSON (ej. `datetime`).
- `with open(...)` con `encoding='utf-8'` para garantizar el cierre y la codificación correcta.
- `pathlib.Path` para construir rutas portables entre sistemas operativos.
- Captura específica de excepciones: `FileNotFoundError`, `json.JSONDecodeError`, `TypeError` (serialización), `PermissionError`.
- Docstrings PEP 257 con `Args`, `Returns` y `Raises`.

## Entrega

- **Google Doc:** https://docs.google.com/document/d/1z5OoDNrPmwSUIcVogt0JXM0NOrbX9HtG35Smx5wUX7M/edit?usp=sharing
- **Nota recibida:** **81% — Aprobado**

### Comentarios del corrector

El trabajo demuestra una excelente capacidad técnica y un dominio sólido de la biblioteca `json` en Python. La implementación del código y el manejo de archivos son impecables, incluyendo soluciones para tipos no serializables y un robusto sistema de excepciones. Sin embargo, el componente teórico de justificación y comparación con otras alternativas es prácticamente inexistente, lo que afecta la calificación final.

**Puntos fuertes**

- Implementación técnica de alta calidad con modularización clara y uso de docstrings.
- Manejo avanzado de tipos no serializables utilizando el parámetro `default` de `json.dump`.
- Gestión de archivos siguiendo todas las mejores prácticas (`with`, `encoding`, `pathlib`).
- Control de errores exhaustivo que cubre múltiples escenarios de fallo.

**Correcciones**

- Incluir una tabla comparativa o una breve sección de texto analizando cuándo es preferible JSON sobre Pickle o YAML.
- Asegurarse de cumplir con la parte de la rúbrica dedicada a la justificación teórica, ya que es fundamental para el análisis de datos estructurados.

**Sugerencias**

- Redactar una sección teórica donde se comparen las ventajas de JSON (interoperabilidad, legibilidad) frente a otros formatos como XML o CSV.
- Investigar la contraparte del manejo de `datetime`: cómo usar el parámetro `object_hook` en `json.load` para reconstruir automáticamente objetos `datetime` al leer el archivo.
