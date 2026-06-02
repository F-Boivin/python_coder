# TP Final Módulo 9 — Biblioteca: aplicación Django con CRUD, CBV y autenticación

Proyecto integrador del Módulo 9 del curso de Python de Coderhouse. Es una aplicación Django funcional que gestiona un catálogo de libros y autores, con autenticación de usuarios, CRUD completo mediante Class-Based Views, protección de vistas con mixins, panel admin personalizado y documentación reproducible.

## Stack y dependencias

- **Python 3.10+** (recomendado 3.12)
- **Django 5.x**
- **SQLite** (incluido en Python, no requiere instalación)
- **Bootstrap 5** (cargado por CDN, no requiere descarga)

No hay otras dependencias externas.

## Setup paso a paso (reproducible)

### 1. Clonar el repositorio

```bash
git clone https://github.com/F-Boivin/python_coder.git
cd python_coder/TP_Modulo_9_Final
```

### 2. Crear y activar entorno virtual

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (cmd):**

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

El prompt cambia y muestra `(.venv)` al inicio. Eso indica que el venv está activo.

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Aplicar migraciones

```bash
python manage.py migrate
```

Esto crea la base SQLite (`db.sqlite3`) con todas las tablas: las del proyecto (`Autor`, `Libro`) y las de Django (`User`, `Group`, `Session`, etc.).

### 5. Crear superusuario

```bash
python manage.py createsuperuser
```

Para uso del corrector, **se sugieren las siguientes credenciales de prueba**:

| Campo | Valor |
|---|---|
| Username | `admin` |
| Email | `admin@biblioteca.local` |
| Password | `Admin123!` |

> Estas credenciales son solo de desarrollo. En un entorno real, jamás deberían estar documentadas en el README.

### 6. (Opcional) Cargar datos de ejemplo desde el shell

```bash
python manage.py shell
```

```python
from catalogo.models import Autor, Libro
borges = Autor.objects.create(nombre="Jorge Luis", apellido="Borges", nacionalidad="Argentina")
cortazar = Autor.objects.create(nombre="Julio", apellido="Cortázar", nacionalidad="Argentina")
Libro.objects.create(titulo="Ficciones", autor=borges, fecha_publicacion="1944-01-01")
Libro.objects.create(titulo="El Aleph", autor=borges, fecha_publicacion="1949-01-01")
Libro.objects.create(titulo="Rayuela", autor=cortazar, fecha_publicacion="1963-01-01")
exit()
```

### 7. Levantar el servidor

```bash
python manage.py runserver
```

El servidor queda en `http://127.0.0.1:8000/`.

## URLs disponibles

| URL | Descripción | Auth |
|---|---|---|
| `/` | Catálogo de libros (listado) | Público |
| `/libros/<id>/` | Detalle de un libro | Público |
| `/libros/nuevo/` | Formulario para crear libro | Login |
| `/libros/<id>/editar/` | Formulario para editar libro | Login + ser creador |
| `/libros/<id>/eliminar/` | Confirmación de borrado | Login + ser creador |
| `/autores/` | Listado de autores | Público |
| `/autores/<id>/` | Detalle de autor con sus libros | Público |
| `/autores/nuevo/` | Formulario para crear autor | Login |
| `/autores/<id>/editar/` | Formulario para editar autor | Login |
| `/autores/<id>/eliminar/` | Confirmación de borrado | Login |
| `/usuarios/login/` | Inicio de sesión | Público |
| `/usuarios/logout/` | Cierre de sesión | Login |
| `/usuarios/registro/` | Alta de nuevo usuario | Público |
| `/admin/` | Panel de administración | Superusuario |

## Estructura del proyecto

```
TP_Modulo_9_Final/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── biblioteca/                # Configuración del proyecto
│   ├── settings.py            # DB, auth URLs, INSTALLED_APPS, etc.
│   ├── urls.py                # Delega a apps
│   ├── asgi.py / wsgi.py
│   └── __init__.py
├── catalogo/                  # App principal: Autor y Libro
│   ├── models.py              # Autor, Libro
│   ├── views.py               # 10 CBVs (5 por modelo, CRUD completo)
│   ├── urls.py                # 11 rutas
│   ├── forms.py               # AutorForm, LibroForm
│   ├── admin.py               # ModelAdmin avanzado + admin actions
│   ├── tests.py               # Tests smoke
│   ├── apps.py
│   └── migrations/
└── usuarios/                  # App de autenticación
    ├── views.py               # RegistroView custom
    ├── urls.py                # login, logout, registro
    ├── forms.py               # RegistroForm con email obligatorio
    ├── apps.py
    └── migrations/

templates/
├── base.html                  # Layout con Bootstrap + navbar dinámico
├── catalogo/                  # 8 templates para CRUD de Libro y Autor
│   ├── libro_list.html        # Con paginación
│   ├── libro_detail.html
│   ├── libro_form.html        # Reusado por Create y Update
│   ├── libro_confirm_delete.html
│   ├── autor_list.html
│   ├── autor_detail.html      # Muestra libros del autor
│   ├── autor_form.html
│   └── autor_confirm_delete.html
└── usuarios/
    ├── login.html
    └── registro.html
```

## Arquitectura de permisos

Tres niveles de acceso, implementados con mixins de `django.contrib.auth.mixins`:

| Operación | Mixin aplicado | Razón |
|---|---|---|
| Listar / ver | (ninguno) | Catálogo público |
| Crear libro/autor | `LoginRequiredMixin` | Solo usuarios registrados pueden agregar contenido |
| Editar/borrar libro | `LoginRequiredMixin` + `UserPassesTestMixin` | Solo el creador puede modificar su libro |
| Editar/borrar autor | `LoginRequiredMixin` | Cualquier usuario logueado (los autores son recursos compartidos) |
| Admin (`/admin/`) | `is_staff` (built-in) | Configurado por Django automáticamente |

`UserPassesTestMixin` implementa `test_func()` que devuelve `True` si el usuario actual es el creador del libro:

```python
def test_func(self):
    libro = self.get_object()
    return self.request.user == libro.creado_por
```

Si devuelve `False`, Django responde con 403 (Forbidden) en lugar de 302 redirect.

## Optimizaciones de rendimiento aplicadas

Lección incorporada del feedback del TP 9d (ModelAdmin): considerar el impacto en SQL al diseñar vistas y admin.

### `select_related` en `LibroListView` y `LibroDetailView`

```python
def get_queryset(self):
    return Libro.objects.select_related("autor").all()
```

Sin esto, renderizar `{{ libro.autor }}` en una lista de 100 libros dispararía **100 queries adicionales** (problema N+1). Con `select_related`, Django hace **un JOIN** y trae todo en una sola query.

### `prefetch_related` en `AutorDetailView`

```python
def get_queryset(self):
    return Autor.objects.prefetch_related("libros")
```

Para la relación inversa (autor → muchos libros), `select_related` no funciona (no es FK directo). `prefetch_related` hace una segunda query con `IN (...)` y arma el cache en memoria. Sigue siendo O(2) queries en lugar de O(1 + N).

### `list_select_related` en `LibroAdmin`

```python
list_select_related = ("autor", "creado_por")
```

Aplica el mismo principio al admin. Sin esto, el listado del admin con 25 libros por página haría 50 queries extra (una por libro × dos FK). Con `list_select_related`, todo en una sola query con JOIN.

### `paginate_by` en listados

`LibroListView` usa `paginate_by = 10`, `AutorListView` usa `paginate_by = 20`. Esto limita el tamaño máximo de cualquier query de listado a una cantidad fija, independiente de cuántos registros tenga la base.

## Personalizaciones del admin

| Atributo | Valor | Razón |
|---|---|---|
| `list_display` | Columnas relevantes + `cantidad_libros` (calculado en autor) | Toda la info clave en la lista sin entrar al detalle |
| `search_fields` | Incluye `autor__apellido` con sintaxis `__` | Búsqueda atravesando la relación FK |
| `list_filter` | Booleano, fecha, FK | Las tres formas de filtro discreto |
| `list_select_related` | `("autor", "creado_por")` | Optimización SQL para list_display con FK |
| `list_editable` | `("disponible",)` | Toggle rápido de disponibilidad sin entrar al form |
| `actions` | `marcar_disponibles`, `marcar_no_disponibles` | Operaciones batch para muchos libros a la vez |
| `readonly_fields` | `("creado_en", "actualizado_en")` | Timestamps inmutables |

## Verificación de la entrega

### Tests automáticos

```bash
python manage.py test catalogo
```

Corre 4 tests smoke que validan:

- Los modelos crean instancias y `__str__` funciona.
- El listado público responde 200.
- La vista de creación rechaza usuarios anónimos (302 redirect a login).
- La vista de creación con login responde 200.

### Checklist manual

- [ ] `python manage.py runserver` arranca sin errores.
- [ ] `/` muestra el catálogo de libros.
- [ ] `/admin/` permite login con el superusuario y muestra `Libros` y `Autores`.
- [ ] `/usuarios/registro/` permite crear un usuario nuevo.
- [ ] Crear un libro estando logueado: aparece `creado_por = mi_usuario`.
- [ ] Editar/borrar un libro: solo funciona si soy el creador (`UserPassesTestMixin`).
- [ ] Logout: vuelve al listado público.

## Cumplimiento de la consigna

| Requisito de la consigna | Dónde se cumple |
|---|---|
| Modelos correctamente definidos y migrados | `catalogo/models.py` + `catalogo/migrations/0001_initial.py` |
| CRUD con Class-Based Views | `catalogo/views.py` — 5 CBV por modelo (List, Detail, Create, Update, Delete) × 2 modelos = 10 vistas |
| URLs para cada vista | `catalogo/urls.py` — 11 rutas |
| Autenticación: registro, login, logout | `usuarios/` — `RegistroView` custom + `LoginView`/`LogoutView` built-in |
| Mixins para proteger vistas sensibles | `LoginRequiredMixin` en Create/Update/Delete + `UserPassesTestMixin` para owner-only |
| Registrar modelos en admin con personalización | `catalogo/admin.py` — `LibroAdmin` y `AutorAdmin` con `ModelAdmin` avanzado |
| README detallado con setup reproducible | Este archivo, secciones 1-7 |
| Superusuario de prueba con credenciales conocidas | Sección "Crear superusuario" |
| Repositorio Git con todo el código | https://github.com/F-Boivin/python_coder/tree/main/TP_Modulo_9_Final |
| Bonus | Tests smoke, paginación, select_related/prefetch_related, admin actions |

## Conceptos del Módulo 9 aplicados

| Unidad | Concepto | Dónde |
|---|---|---|
| U1 — CRUD + setup | venv, settings, SQLite | `requirements.txt`, `settings.py` |
| U2 — Modelos y migraciones | `models.Model`, FK, makemigrations | `catalogo/models.py` |
| U3 — Admin básico | `admin.site.register` | `catalogo/admin.py` |
| U4-6 — ListView + DetailView | CBV genéricas con `context_object_name` | `LibroListView`, `LibroDetailView` |
| U7 — CreateView + UpdateView | CBV con `form_class`, `success_url`, `form_valid` | `LibroCreateView`, `LibroUpdateView` |
| U8 — ModelAdmin avanzado | `list_display`, `search_fields`, `list_filter`, `list_select_related`, actions | `catalogo/admin.py` |
| U9-11 — Auth y mixins | `LoginRequiredMixin`, `UserPassesTestMixin`, vistas auth built-in | `catalogo/views.py` + `usuarios/` |

## Entrega

- **Plataforma:** Google Doc con código + link al repo GitHub (la plataforma de Coder no permite links directos a GitHub, solo Google Docs o apps desplegadas).
- **Repositorio:** https://github.com/F-Boivin/python_coder/tree/main/TP_Modulo_9_Final
- **Nota recibida:** **95% — Aprobado** ⭐

### Comentarios del corrector

El trabajo presentado es excepcional, cubriendo todos los aspectos del Módulo 9 con un alto nivel de detalle técnico y profesionalismo. La aplicación cumple con todos los requisitos funcionales y extra de la consigna, demostrando una excelente comprensión de Django.

**Puntos fuertes**

- Uso avanzado de CBV y optimizaciones de consultas (`select_related`, `prefetch_related`).
- Implementación sólida de seguridad usando mixins y control de acceso basado en el creador.
- Documentación técnica impecable, clara y orientada a la reproducibilidad.

**Para mejorar**

- Integrar validaciones más complejas en el backend para los modelos, más allá de lo requerido, enriquecería aún más el sistema.
- Explorar pruebas unitarias (tests) más avanzadas usando `pytest-django`.
- Considerar el despliegue del proyecto en servicios como Render o Railway para practicar el flujo CI/CD.

## Notas adicionales

- **Entorno:** desarrollado en la terminal integrada de **VS Code**.
- **Commits:** prefijo Conventional Commits (`feat:`, `docs:`).
- **Reproducibilidad:** seguir la sección "Setup paso a paso" debería levantar el proyecto en menos de 2 minutos en cualquier máquina con Python 3.10+.
