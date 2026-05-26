# TP Final Módulo 7 — Herramienta de procesamiento y persistencia

Trabajo práctico integrador de la **Unidad 8 del Módulo 7** del curso de Python de Coderhouse. Integra los temas vistos en todo el módulo: scripts, módulos, paquetes, manejo de archivos, JSON y CSV.

## Consigna

Construir una herramienta en Python que:

1. Esté organizada en un paquete propio (`procesador`) con al menos dos módulos.
2. Implemente lectura de datos desde JSON o CSV.
3. Implemente escritura de datos procesados en JSON o CSV.
4. Tenga un `main.py` que use el patrón `if __name__ == "__main__":`.
5. Use `with` en todos los accesos a archivos.
6. Maneje errores en lectura y escritura.
7. Muestre mensajes claros de inicio, proceso y finalización en consola.
8. Documente cada módulo y función.

## Escenario elegido

Procesamiento de un **registro de ventas** (CSV de entrada con fecha, producto, cantidad y precio unitario). La herramienta:

- Calcula el total facturado por producto.
- Identifica los top 3 productos por facturación.
- Genera **dos reportes**: un JSON detallado y un CSV tabular ordenado.

## Estructura del proyecto

```
TP_Modulo_7_Final/
├── procesador/                ← Paquete propio
│   ├── __init__.py            ← Expone la API pública del paquete
│   ├── lectura.py             ← leer_json, leer_csv, parse_fechas
│   ├── escritura.py           ← escribir_json, escribir_csv
│   └── procesamiento.py       ← calcular_totales_por_producto, top_n_productos
├── datos/
│   └── ventas.csv             ← Archivo de entrada (15 registros)
├── main.py                    ← Script principal con __name__ == "__main__"
├── reporte.json               ← Generado al ejecutar
├── reporte.csv                ← Generado al ejecutar
└── README.md
```

> **Decisión de diseño:** separé el paquete en **3 módulos en lugar de 2** (lectura / procesamiento / escritura) para reforzar el principio de responsabilidad única. El módulo `procesamiento` es totalmente puro (sin I/O), lo que facilita pruebas unitarias y reutilización.

## Cómo ejecutar

```bash
cd TP_Modulo_7_Final
python main.py
```

En Windows, si la consola no muestra bien las tildes:

```powershell
chcp 65001
python main.py
```

## Salida esperada

```
============================================================
Iniciando procesamiento de registros de ventas...
============================================================
[OK] 15 registros leídos desde 'ventas.csv'.
[..] Calculando totales por producto...
[OK] 6 productos distintos procesados.
[OK] Reporte JSON guardado en 'reporte.json'.
[OK] Reporte CSV guardado en 'reporte.csv'.

============================================================
Resumen del procesamiento
============================================================
Registros procesados:    15
Productos distintos:     6
Total facturado:         $5,814,000.00

Top 3 productos:
  1. Notebook        $4,250,000.00
  2. Monitor         $540,000.00
  3. Teclado         $315,000.00

============================================================
Procesamiento finalizado correctamente.
============================================================

[Demo extra] Releyendo reporte.json con object_hook:
  Tipo de 'generado_en': datetime
  Valor: 2026-05-26 14:30:00.123456
```

## Justificación teórica

### ¿Por qué este escenario usa CSV de entrada y JSON+CSV de salida?

- **CSV como entrada:** las ventas vienen típicamente de exportaciones de ERPs, planillas de Excel o bases de datos relacionales. CSV es el formato universal para datos tabulares planos.
- **JSON como reporte detallado:** permite anidar estructuras (lista de top productos, metadatos del procesamiento, fecha de generación) que CSV no representa bien.
- **CSV como reporte tabular:** facilita que un usuario no técnico abra el resumen en Excel o Google Sheets.

### Comparativa de formatos de persistencia

| Formato | Estructura | Legibilidad humana | Tipos soportados | Caso ideal |
|---------|-----------|--------------------|--------------------|------------|
| **JSON** | Jerárquica (dicts y listas anidadas) | Buena | str, int, float, bool, null, list, dict | Configuraciones, APIs REST, reportes con anidamiento |
| **CSV** | Tabular plana (filas × columnas) | Excelente en Excel/Sheets | Todo se almacena como string | Datos tabulares uniformes, exportar a hojas de cálculo |
| **Pickle** | Cualquier objeto Python | Nula (binario) | Cualquier objeto Python | Cache interno entre ejecuciones del mismo programa Python |
| **YAML** | Jerárquica con indentación | Muy buena | Tipos básicos + tags custom | Archivos de configuración largos (CI/CD, Kubernetes) |
| **XML** | Jerárquica con tags | Media | Strings con esquema opcional | Sistemas legacy, SOAP, intercambio empresarial |

### ¿Cuándo elegir cada uno?

- **JSON** si los datos tienen estructura anidada y necesitan interoperar con otros sistemas (web, APIs, JavaScript).
- **CSV** si son tabulares uniformes y el consumidor puede ser un humano con Excel.
- **Pickle** **solo** para uso interno Python-a-Python (no es seguro abrir pickles ajenos: puede ejecutar código arbitrario).
- **YAML** para configuración legible que humanos van a editar a mano.
- **XML** rara vez para proyectos nuevos; relevante si se integra con sistemas viejos.

### Manejo simétrico de tipos especiales

JSON no tiene un tipo nativo para fechas, pero soporta extensión vía callbacks:

| Dirección | Parámetro | Uso en este proyecto |
|-----------|-----------|----------------------|
| Serializar (`json.dump`) | `default=` | `_serializar_extras` convierte `datetime` → string ISO 8601 |
| Deserializar (`json.load`) | `object_hook=` | `parse_fechas` convierte strings ISO 8601 → `datetime` |

La demo `demo_lectura_inversa()` en `main.py` muestra el ciclo completo.

## Cumplimiento de la consigna

| # | Requisito | Dónde se cumple |
|---|-----------|-----------------|
| 1 | Paquete `procesador` con módulos | `procesador/` con `__init__.py`, `lectura.py`, `escritura.py`, `procesamiento.py` |
| 2 | Lectura desde JSON o CSV | `lectura.leer_json()` y `lectura.leer_csv()` |
| 3 | Escritura a JSON o CSV | `escritura.escribir_json()` y `escritura.escribir_csv()` |
| 4 | `main.py` que importa del paquete | `main.py` línea 18-25 |
| 5 | Patrón `if __name__ == "__main__":` | `main.py` línea final |
| 6 | Uso consistente de `with` | Las 4 funciones de I/O en `lectura.py` y `escritura.py` |
| 7 | Manejo de errores | `try/except` específicos en `main.py` (FileNotFoundError, PermissionError, UnicodeDecodeError, KeyError, ValueError, OSError) |
| 8 | Mensajes claros en consola | Etiquetas `[OK]`, `[..]`, `[ERROR]` + separadores visuales + resumen final |
| 9 | Documentación | Docstring PEP 257 en cada módulo y cada función (con `Args`, `Returns`, `Raises`) |

## Conceptos del módulo aplicados

| Unidad del módulo | Concepto | Dónde aparece |
|--------------------|----------|--------------|
| U1 — Scripts | Patrón `if __name__ == "__main__":` | Final de `main.py` |
| U2 — Módulos | Importación con `from ... import` | `main.py` líneas 18-25 |
| U3 — Paquetes | Estructura con `__init__.py` | `procesador/__init__.py` |
| U4 — Persistencia | Diferencia texto vs binario, encoding UTF-8 | Todas las funciones de I/O |
| U5 — Archivos de texto | `with`, lectura/escritura, manejo de errores | `lectura.py`, `escritura.py` |
| U6 — JSON | `json.dump`, `json.load`, `default=`, `object_hook=` | `escritura.escribir_json`, `lectura.leer_json` |
| U7 — CSV | `csv.DictReader`, `csv.DictWriter`, `newline=''`, delimitadores | `lectura.leer_csv`, `escritura.escribir_csv` |

## Entrega

- **Google Doc:** https://docs.google.com/document/d/13ysNKIxfpUnIPghqOxtVdlWJEM7fpTYJkj5gVbvNhK4/edit?usp=sharing
- **Nota recibida:** **94% — Aprobado**

### Comentarios del corrector

La entrega es sólida y muy cercana a una solución completa: presenta una estructura clara del paquete, persistencia correcta con `with`, control de ejecución adecuado y una descripción detallada del flujo de consola. El documento además incluye el código fuente y una salida esperada bien explicada, por lo que cumple ampliamente con la consigna.

**Puntos fuertes**

- Estructura de paquete bien organizada con módulos separados por responsabilidad.
- Uso correcto de `if __name__ == "__main__":` y funciones bien documentadas.
- Persistencia segura en JSON/CSV con `with`, `json.dump`, `csv.DictWriter` y manejo básico de errores.
- Incluye evidencia textual de la ejecución y resultados esperados con métricas concretas.

**Correcciones**

- Agregar validaciones más finas para datos inválidos o incompletos del CSV.
- Incluir capturas reales de ejecución si la consigna del curso lo requiere.
- Asegurar que el README completo esté visible o incrustado en el documento si debe evaluarse como parte de la evidencia.

**Sugerencias**

- Revisar el flujo con datos de prueba que contengan errores para fortalecer el manejo de excepciones.
- Ejecutar el proyecto y documentar una captura real de consola junto con los archivos generados.
- Mantener la separación de responsabilidades, y considerar sumar tests unitarios básicos para lectura, procesamiento y escritura.
