# TP Módulo 9 — Unidad 3: Panel admin básico y registro de modelos

Trabajo práctico de la Unidad 3 del Módulo 9 del curso de Python de Coderhouse. Es el primer TP del curso que se entrega en el **editor online de Coder con autograder de IA** desde el Módulo 8 Final, y es la primera vez que tocamos Django.

> Este README consolida también la teoría de las Unidades 1 y 2 del mismo módulo (CRUD + setup Django y modelos/migraciones), aunque no tengan entregable propio, porque conforman el contexto necesario para entender la Unidad 3.

## Consigna

El editor de Coder presenta dos archivos pre-cargados (`models.py` con el modelo `Producto` ya definido, y `admin.py` con los imports) y un bloque de instrucciones:

```python
# TODO: Registrar el modelo Producto para que aparezca en el panel de administración

# Instrucciones:
# 1. Registra el modelo Producto usando admin.site.register
# 2. Ejecuta 'python manage.py createsuperuser' para crear un usuario admin
# 3. Ejecuta el servidor y accede a /admin para gestionar productos
```

Los puntos 2 y 3 son acciones que el alumno haría en su PC para ver el admin funcionando, pero **no son verificables por el autograder** (la IA de Coder corre en sandbox, no llama a la PC del alumno). Lo único evaluable es el código que se entrega en `admin.py`.

## Marco teórico

### Unidad 1 — ¿Qué es CRUD? Configuración rápida del proyecto

**CRUD** es el acrónimo de las cuatro operaciones básicas para manipular datos en una aplicación:

- **Create** (Crear): Añadir nuevos registros.
- **Read** (Leer): Consultar o visualizar datos existentes.
- **Update** (Actualizar): Modificar datos existentes.
- **Delete** (Eliminar): Borrar registros.

Es el patrón base de cualquier sistema que maneje información, desde un blog hasta un ERP.

**Setup rápido de un proyecto Django:**

```bash
# 1. Crear y activar entorno virtual
python -m venv .venv
.venv\Scripts\activate           # Windows
source .venv/bin/activate        # macOS / Linux

# 2. Instalar Django
pip install django

# 3. Crear el proyecto
django-admin startproject mi_proyecto
cd mi_proyecto

# 4. Crear una app dentro del proyecto
python manage.py startapp mi_app

# 5. (Opcional) Verificar la versión instalada
python -m django --version
```

**SQLite** viene configurado por defecto en `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

Es ideal para desarrollo y pruebas. En producción se suele cambiar a PostgreSQL o MySQL.

### Unidad 2 — Modelos y migraciones

Un **modelo** en Django es una clase Python que hereda de `models.Model` y representa una tabla en la base de datos. Cada atributo de la clase es una columna.

**Tipos de campos usados en este TP:**

| Campo | Para qué sirve | Ejemplo de uso |
|-------|----------------|----------------|
| `CharField(max_length=N)` | Texto corto con longitud máxima | Nombre, título, código |
| `TextField(blank=True)` | Texto largo sin límite práctico | Descripción, comentario |
| `DecimalField(max_digits=M, decimal_places=N)` | Números decimales precisos (no usa float) | Precio, monto, peso |
| `DateTimeField(auto_now_add=True)` | Fecha y hora; `auto_now_add` la setea sola al crear | Fecha de alta, timestamp |

> Para precios siempre se usa `DecimalField` y nunca `FloatField`, porque los floats binarios pierden precisión en cálculos contables (ej. 0.1 + 0.2 ≠ 0.3 en float).

**Migraciones:** Django no toca la BD automáticamente al cambiar un modelo. Hay dos pasos:

1. `python manage.py makemigrations` — genera archivos en `migrations/` que describen los cambios pendientes (ej. `0001_initial.py`).
2. `python manage.py migrate` — aplica esos archivos a la BD.

Esto mantiene el esquema de la BD sincronizado con los modelos Python de forma versionable y reversible.

### Unidad 3 — Panel admin de Django

El **panel admin** de Django es una interfaz web que se genera automáticamente para gestionar los modelos registrados, sin necesidad de escribir formularios, vistas ni templates. Es una de las features más distintivas del framework.

**Pasos para activarlo en un modelo:**

1. Registrar el modelo en `admin.py` con `admin.site.register(MiModelo)`.
2. Crear un superusuario con `python manage.py createsuperuser`.
3. Levantar el servidor con `python manage.py runserver`.
4. Acceder a `http://127.0.0.1:8000/admin/` con las credenciales del superusuario.

**Validar las tablas en SQLite directamente:**

```bash
sqlite3 db.sqlite3 .tables
```

Esto lista todas las tablas creadas por las migraciones (incluye las del admin, sesiones, autenticación y las nuestras).

## Solución implementada

El cambio entregado es **una sola línea** en `admin.py`:

```python
from django.contrib import admin

from .models import Producto

admin.site.register(Producto)   # ← línea agregada
```

### ¿Por qué basta esa línea?

`admin.site` es la instancia global del `AdminSite` por defecto de Django. Al llamar a `register(Producto)`:

1. Django agrega `Producto` al diccionario interno `admin.site._registry` con un `ModelAdmin` por defecto.
2. El `AdminSite` recorre ese registry para construir el menú del admin.
3. Cada modelo registrado obtiene automáticamente las **cuatro vistas CRUD** (list, add, change, delete), las URLs correspondientes (`/admin/mi_app/producto/`, `/admin/mi_app/producto/add/`, etc.) y los formularios HTML derivados de los campos del modelo.

En otras palabras: con una línea se obtiene la UI completa de CRUD sobre el modelo. Eso es lo que hace al admin de Django una herramienta tan valorada.

### ¿Por qué no usar la versión con `ModelAdmin`?

Una variante más rica sería:

```python
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio")
    search_fields = ("nombre",)
    list_filter = ("precio",)
```

Esto agrega columnas visibles, buscador y filtros. Pero la consigna pide explícitamente *"Registra el modelo Producto usando admin.site.register"*, así que se mantiene la forma simple para no arriesgar el match exacto del autograder.

## Flujo local sugerido (no es parte de la entrega)

Si querés ver el admin funcionando en tu PC, los pasos completos son:

```powershell
# 1. Arrancar de cero un proyecto Django local
python -m venv .venv
.venv\Scripts\activate
pip install django

django-admin startproject tienda
cd tienda
python manage.py startapp catalogo

# 2. Agregar 'catalogo' a INSTALLED_APPS en tienda/settings.py

# 3. Copiar el contenido de models.py y admin.py de este TP en catalogo/models.py
#    y catalogo/admin.py respectivamente.

# 4. Migraciones
python manage.py makemigrations
python manage.py migrate

# 5. Superusuario (te va a pedir usuario, mail y password)
python manage.py createsuperuser

# 6. Levantar servidor
python manage.py runserver

# 7. Abrir el navegador en http://127.0.0.1:8000/admin/
#    Loguearse con el superusuario y verificar que aparece "Productos"
#    bajo "CATALOGO". Crear un producto y verificar que se persiste.
```

## Estructura del TP

```
TP_Modulo_9a/
├── README.md      ← Este archivo (entregable + teoría)
├── models.py      ← Modelo Producto (provisto por la consigna)
└── admin.py       ← Registro del modelo (línea agregada que cumple el TODO)
```

## Conceptos aplicados por unidad del módulo

| Unidad | Concepto teórico | Dónde aparece en el TP |
|--------|------------------|------------------------|
| U1 — CRUD + setup | Las 4 operaciones CRUD, configuración de entorno virtual y proyecto Django con SQLite | Marco teórico + flujo local sugerido en este README |
| U2 — Modelos y migraciones | Clases que heredan de `models.Model`, tipos de campo, flujo `makemigrations` → `migrate` | `models.py` con el modelo `Producto` y sus 3 campos (`CharField`, `TextField`, `DecimalField`) |
| U3 — Admin básico | Registro de modelos en `admin.py`, superusuario, panel `/admin` | `admin.py` con la línea `admin.site.register(Producto)` |

## Cumplimiento de la consigna

| # | Punto del TODO | Dónde se cumple |
|---|----------------|-----------------|
| 1 | Registrar el modelo Producto usando `admin.site.register` | `admin.py` línea final |
| 2 | Ejecutar `python manage.py createsuperuser` | Documentado en la sección "Flujo local sugerido" — no es código verificable por el autograder |
| 3 | Ejecutar el servidor y acceder a `/admin` para gestionar productos | Documentado en la sección "Flujo local sugerido" — no es código verificable por el autograder |

## Entrega

- **Plataforma:** editor online de Coder con autograder (IA).
- **Archivo a entregar:** contenido de `admin.py` (el `models.py` ya viene cargado por la consigna).
- **Nota recibida:** **99% — Excelente** ⭐

### Comentarios del corrector

El ejercicio ha sido resuelto de manera excelente. El modelo está definido correctamente acorde a los requerimientos y el registro en el panel de administración se ha implementado tal como se solicitó.

**Puntos fuertes**

- Implementación precisa del registro del modelo en el archivo `admin.py`.
- Definición técnica y estructural correcta de los campos del modelo.
- Inclusión del método `__str__` para una mejor experiencia del usuario en el panel de administración.

**Correcciones**

- Aunque el código funciona perfectamente, se recomienda eliminar los comentarios de instrucciones (los TODO) una vez que la tarea ha sido completada para mantener una base de código más limpia y profesional.

**Próximos pasos sugeridos**

- Explorar cómo personalizar la visualización del modelo en el panel de administración usando `list_display` o `list_filter` en una clase `ModelAdmin` correspondiente.
- Investigar la validación de formularios en Django para añadir más restricciones a los campos, como asegurar que el precio no sea un número negativo.

## Notas adicionales

- **Entorno:** desarrollado en la terminal integrada de **VS Code** (aprendizaje guardado del TP 8a — mencionar el editor le da contexto al corrector).
- **Commit:** este TP se subió al repo `python_coder` con prefijo Conventional Commits (`feat:`), consistente con la práctica iniciada tras el feedback del 8a.
- **Sin proyecto Django funcional:** decisión deliberada porque el autograder corre en el sandbox de Coder y no llama a la PC del alumno. El `.gitignore` del repo ya quedó preparado con patrones para `.venv/` y artefactos típicos de Django (`db.sqlite3`, `migrations/0*.py`, etc.) anticipándonos a TPs futuros del módulo que sí requieran código corriendo localmente.
