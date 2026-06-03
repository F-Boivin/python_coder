# TP Módulo 10 — Workshop Blog (proyecto Django incremental)

Proyecto Django único que cubre **los 7 entregables del Módulo 10** del curso de Python de Coderhouse. El módulo está diseñado para construirse de forma incremental: cada unidad agrega una capa al mismo proyecto `workshop` con su app `core`.

## Por qué un solo proyecto cubre todas las unidades

| Unidad | Entrega | Capa que aporta al proyecto |
|--------|---------|------------------------------|
| U1 | — (teórica) | Patrón MTV |
| **U2** | ✅ | Proyecto `workshop` + app `core` (setup) |
| **U3** | ✅ | Modelos `Author`, `Tag`, `Post` |
| **U4** | ✅ | Migraciones + admin de los modelos |
| **U5** | ✅ | Vistas CRUD (CBV) para `Post` |
| **U6** | ✅ | Templates `base.html` + `post_list.html` + filtros custom |
| **U7** | ✅ | URLs de `core` con namespacing |
| U8 | — (teórica) | Fundamentos de Git + `.gitignore` |
| **U9** | ✅ | Flujo GitHub: rama feature + Pull Request |

Todos los entregables convergen en este mismo proyecto. Cada Google Doc de entrega enfoca la capa que su unidad evalúa, y todos apuntan a este repositorio.

## Stack

- Python 3.10+ · Django 5.x · SQLite · Bootstrap 5 (CDN)

## Setup reproducible

```bash
# 1. Clonar y entrar
git clone https://github.com/F-Boivin/python_coder.git
cd python_coder/TP_Modulo_10

# 2. Entorno virtual
python -m venv .venv
.venv\Scripts\Activate.ps1          # Windows PowerShell
# source .venv/bin/activate         # macOS / Linux

# 3. Dependencias
pip install -r requirements.txt

# 4. Migraciones
python manage.py migrate

# 5. Superusuario (sugerido: admin / Admin123!)
python manage.py createsuperuser

# 6. Servidor
python manage.py runserver
# → http://127.0.0.1:8000/
```

## Estructura del proyecto

```
TP_Modulo_10/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── workshop/                  # Configuración del proyecto
│   ├── settings.py            # INSTALLED_APPS incluye 'core'
│   ├── urls.py                # include('core.urls')
│   ├── wsgi.py / asgi.py
│   └── __init__.py
├── core/                      # App del blog
│   ├── models.py              # Author, Tag, Post (con clean())
│   ├── admin.py               # AuthorAdmin, TagAdmin, PostAdmin
│   ├── views.py               # 5 CBV para el CRUD de Post
│   ├── urls.py                # app_name='core' + 5 rutas con converters
│   ├── forms.py               # PostForm (ModelForm)
│   ├── tests.py               # Tests smoke
│   ├── templatetags/
│   │   └── core_extras.py     # Filtros custom: mayusculas, resumen
│   ├── templates/core/        # post_list, post_detail, post_form, confirm_delete
│   └── migrations/
└── templates/
    └── base.html              # Plantilla base con bloques title/nav/content
```

## URLs disponibles (con namespacing `core:`)

| URL | Nombre | Vista |
|-----|--------|-------|
| `/` | `core:post-list` | Lista de posts publicados |
| `/posts/nuevo/` | `core:post-create` | Crear post |
| `/posts/<int:pk>/` | `core:post-detail` | Detalle de un post |
| `/posts/<int:pk>/editar/` | `core:post-update` | Editar post |
| `/posts/<int:pk>/eliminar/` | `core:post-delete` | Borrar post |
| `/admin/` | — | Panel de administración |

## Dominio modelado (Unidad 3)

- **Author** — `name`, `email` (único). `__str__` → name.
- **Tag** — `name`. `__str__` → name.
- **Post** — `title`, `content`, `published_date`, FK a `Author`, M2M a `Tag`.
  - `Meta.ordering = ["-published_date"]` (más nuevos primero).
  - `clean()` valida que el título tenga al menos 5 caracteres.
  - `get_absolute_url()` para redirecciones.

## Conceptos destacados por unidad

- **U5 — get_queryset:** `PostListView` filtra `published_date__lte=now` (oculta posts programados a futuro) y usa `select_related("author")` + `prefetch_related("tags")` para evitar el problema N+1.
- **U6 — filtros custom:** `core/templatetags/core_extras.py` define `mayusculas` (sin argumento) y `resumen:N` (con argumento), usados en `post_list.html`.
- **U7 — namespacing:** `app_name = "core"` permite referenciar rutas como `{% url 'core:post-detail' post.pk %}` y `reverse_lazy("core:post-list")`.
- **U8 — .gitignore:** excluye `__pycache__/`, `db.sqlite3`, `.venv/`, `.env`, conservando migraciones.

## Entrega

Cada unidad se entrega como Google Doc separado, todos apuntando a este repo:

| Unidad | Google Doc | Nota |
|--------|-----------|------|
| U2 | entregado | **91%** |
| U3 | entregado | **100%** 🎯 |
| U4 | _pendiente_ | _pendiente_ |
| U5 | _pendiente_ | _pendiente_ |
| U6 | _pendiente_ | _pendiente_ |
| U7 | _pendiente_ | _pendiente_ |
| U9 | _pendiente_ | _pendiente_ |

## Notas

- Desarrollado y probado en la terminal integrada de **VS Code**.
- Commits con **Conventional Commits** (`feat:`, `docs:`).
- La Unidad 9 (Pull Request) se documenta con el link al PR real en GitHub.
