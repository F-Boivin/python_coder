# TP Final Módulo 8 — Validador de flujo Git + Django

Trabajo práctico integrador del Módulo 8 del curso de Python de Coderhouse. A diferencia de los TPs anteriores, este se entrega como **código pegado en el editor online de Coder** (no Google Doc), y se evalúa automáticamente con un autograder.

## Consigna

Implementar un programa Python que reciba por entrada estándar una secuencia de N eventos simulando el flujo de trabajo de un proyecto Django gestionado con Git, y determine si la secuencia cumple las reglas de un repositorio válido:

- El repositorio debe iniciar con `INIT`.
- Debe existir al menos una rama `feature` creada, con commits, y mergeada a `main`.
- Los mensajes de commit no pueden estar vacíos.
- Deben crearse archivos clave: `views.py`, `template.html`, `requirements.txt`, `README.md`.
- Debe haber al menos un `PUSH` al remoto.
- Debe haber al menos un `PULL_REQUEST`.

**Tipos de evento reconocidos:**
`INIT`, `CREATE_BRANCH <nombre>`, `CHECKOUT_BRANCH <nombre>`, `CREATE_FILE <nombre>`, `COMMIT <mensaje>`, `PUSH`, `PULL_REQUEST`.

**Salida:** `VALID` o `INVALID`.

## Contexto

Este TP fue entregado en su momento al autograder de Coder y obtuvo **77% (Bueno)** — nota que queda como definitiva porque la plataforma del curso ya no permite reenvíos sobre este ejercicio. El código que vive en este repositorio es una **reescritura posterior** que incorpora las tres observaciones del corrector, como ejercicio de portfolio y para fijar los aprendizajes:

| # | Observación del corrector | Cómo se corrige en esta versión |
|---|-----------------------------|---------------------------------|
| 1 | Aumentar el rigor en la validación de archivos para incluir `requirements.txt` | Ahora se requieren **los 4 archivos** (`views.py`, `template.html`, `requirements.txt`, `README.md`), no solo dos. Ver el set `ARCHIVOS_REQUERIDOS` |
| 2 | La lógica de merge no debe depender solo del nombre de rama, sino de la persistencia de commits | El merge se detecta solo si la rama feature tuvo **al menos un commit** antes de volver a main. Se chequea `commits_por_rama[rama_actual] > 0` |
| 3 | Manejo de errores con retorno temprano (`print('INVALID'); return`) en lugar de acumular flags al final | La función `validar()` hace `return False, motivo` apenas detecta una violación. No espera al final del recorrido salvo para las cuatro condiciones globales (merge, archivos, push, PR) que solo se pueden evaluar después de procesar todo |

## Estrategia de solución

### Estructura

Una única función `validar(eventos)` pura (sin I/O) que modela el estado del repositorio durante el recorrido:

```python
init_hecho        # bool
rama_actual       # str | None
ramas_creadas     # set[str], inicializado con {"main"} al hacer INIT
archivos          # set[str]
commits_por_rama  # defaultdict(int)
ramas_mergeadas   # set[str]
hubo_push         # bool
hubo_pr           # bool
```

Y una función `main()` que lee stdin, llama a `validar()` e imprime `VALID`/`INVALID`.

### Reglas implementadas

| Tipo de regla | Cuándo se viola | Comportamiento |
|---------------|-----------------|----------------|
| INIT debe ser primer evento | Otro tipo antes, o INIT en posición ≠ 0 | Retorno temprano |
| Evento previo a INIT | Cualquier tipo ≠ INIT antes que INIT | Retorno temprano |
| CREATE_BRANCH sin nombre | Detalle vacío | Retorno temprano |
| CHECKOUT_BRANCH a rama inexistente | Rama no creada antes | Retorno temprano |
| COMMIT con mensaje vacío | `detalle == ""` | Retorno temprano |
| PUSH sin commits | `sum(commits_por_rama.values()) == 0` | Retorno temprano |
| Tipo desconocido | No matchea ninguno de los 7 válidos | Retorno temprano |
| Sin merge real | No hay feature branch con commits + vuelta a main | Validación final |
| Faltan archivos | Algún archivo de `ARCHIVOS_REQUERIDOS` no creado | Validación final |
| Sin PUSH o sin PR | Flags `hubo_push` o `hubo_pr` en False | Validación final |

### Detección de merge "rigurosa"

La consigna no define un evento explícito `MERGE`. Se infiere el merge cuando:

1. Hubo un `CHECKOUT_BRANCH feature_X` previo.
2. Mientras estábamos en `feature_X` se ejecutó al menos un `COMMIT` (esto sube `commits_por_rama["feature_X"]`).
3. Luego se hizo `CHECKOUT_BRANCH main`.

En ese momento, `feature_X` se agrega al set `ramas_mergeadas`. La validación final exige que ese set no esté vacío.

> Esta lógica es más rigurosa que mirar solo el historial de nombres de rama — exige **persistencia real de commits** en la feature branch, como pidió el corrector.

## Cómo ejecutar localmente

Desde la terminal integrada de VS Code, parado en esta carpeta:

```bash
python main.py
```

El script lee de stdin: primero un entero N, luego N líneas con los eventos. Tipear `Ctrl+Z` + Enter en Windows (`Ctrl+D` en Linux/macOS) si se quiere cerrar antes de las N líneas.

Más práctico: usar un archivo de entrada con redirect:

```bash
python main.py < ejemplo_valid.txt
```

## Ejemplos

### Ejemplo VALID (incluye los 4 archivos requeridos)

**Entrada:**
```
12
INIT
CREATE_FILE README.md
CREATE_FILE requirements.txt
CREATE_BRANCH feature1
CHECKOUT_BRANCH feature1
CREATE_FILE views.py
CREATE_FILE template.html
COMMIT Agregar vista y template
CHECKOUT_BRANCH main
COMMIT Preparar entorno base del proyecto
PUSH
PULL_REQUEST
```

**Salida:** `VALID`

### Ejemplo INVALID por faltar archivos

**Entrada:**
```
10
INIT
CREATE_BRANCH feature1
CHECKOUT_BRANCH feature1
CREATE_FILE views.py
CREATE_FILE template.html
COMMIT Añadir vista y template
CHECKOUT_BRANCH main
COMMIT Preparar entorno
PUSH
PULL_REQUEST
```

**Salida:** `INVALID`
**Motivo interno:** "Faltan archivos requeridos: README.md, requirements.txt."

> Este es exactamente el ejemplo del enunciado de la consigna. La versión estricta (siguiendo al corrector) lo marca como INVALID porque no se crean `requirements.txt` ni `README.md`. Es un riesgo asumido — si el autograder usa este ejemplo como test fijo esperando `VALID`, se perdería ese caso. La hipótesis es que el grader premia más el rigor (de ahí el 77% original al ser laxo).

### Ejemplo INVALID por mensaje de commit vacío

**Entrada:**
```
6
INIT
CREATE_FILE README.md
CREATE_FILE requirements.txt
CREATE_FILE views.py
CREATE_FILE template.html
COMMIT
```

**Salida:** `INVALID`
**Motivo interno:** "Evento 6: COMMIT con mensaje vacío."

## Casos de prueba cubiertos

Los siguientes 8 casos se probaron manualmente durante el desarrollo y todos retornan el resultado esperado:

| # | Caso | Resultado |
|---|------|-----------|
| 1 | Flujo completo correcto con los 4 archivos | VALID |
| 2 | Ejemplo del enunciado (faltan 2 archivos) | INVALID |
| 3 | COMMIT con mensaje vacío | INVALID |
| 4 | CREATE_FILE antes de INIT | INVALID |
| 5 | Feature branch sin commits, vuelta a main | INVALID (no hay merge real) |
| 6 | CHECKOUT_BRANCH a rama no creada | INVALID |
| 7 | PUSH antes de cualquier commit | INVALID |
| 8 | Flujo válido pero sin PULL_REQUEST | INVALID |

## Entrega

- **Plataforma:** editor online integrado de Coder (autograder), no Google Doc.
- **Nota final:** **77% — Bueno** (la plataforma no permite reentrega de este ejercicio).
- **Estado del código en este repo:** versión mejorada post-feedback, conservada como referencia de portfolio. No fue evaluada por el corrector.

## Notas adicionales

- **Entorno:** desarrollado y probado en la terminal integrada de **VS Code** (Windows, PowerShell, Python 3.x).
- **Commits del repo:** este TP se subió al repositorio `python_coder` usando el estándar **Conventional Commits** (`feat: ...`), aprendizaje incorporado del feedback del TP 8a.
- **Estilo:** docstring PEP 257 en módulo y función, con secciones Args/Returns explícitas.
