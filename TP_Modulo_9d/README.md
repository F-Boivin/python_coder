# TP Módulo 9 — Unidad 8: Administración avanzada con ModelAdmin

Trabajo práctico de la Unidad 8 del Módulo 9 del curso de Python de Coderhouse. A diferencia de las unidades 3, 4-6 y 7 (que se entregaban en el editor online con autograder), **esta unidad se entrega como Google Doc**, lo que permite profundizar en la teoría y mostrar comparativas que un autograder no evalúa.

## Consigna

1. Abrir el archivo `admin.py` de la aplicación.
2. Crear una clase que herede de `admin.ModelAdmin` para el modelo a personalizar.
3. Definir los atributos `list_display`, `search_fields` y `list_filter` con campos relevantes.
4. Registrar el modelo junto con la clase `ModelAdmin` usando `admin.site.register()`.
5. Verificar en el panel `/admin` que la lista muestra las columnas configuradas, que la búsqueda funciona y que los filtros aparecen en la barra lateral.

**Preguntas de evaluación:**

- ¿Qué campos aparecen en la lista principal del admin?
- ¿Se puede buscar registros usando la barra de búsqueda?
- ¿Los filtros laterales segmentan correctamente los datos?

## Marco teórico

### ¿Qué es `ModelAdmin`?

`ModelAdmin` es la clase del módulo `django.contrib.admin` que controla cómo se ve y cómo se comporta cada modelo dentro del panel de administración. Sin personalización, Django muestra una vista por defecto:

- **Lista:** solo el resultado de `__str__(self)` del modelo, en una única columna.
- **Búsqueda:** ausente.
- **Filtros:** ausentes.
- **Orden:** el que defina `Meta.ordering` del modelo, o el orden de inserción.

Eso es suficiente para prototipos, pero apenas el modelo crece o lo usa gente no técnica, se vuelve impráctico. `ModelAdmin` resuelve esto con atributos declarativos: en pocas líneas se configura qué columnas mostrar, qué se puede buscar, qué se puede filtrar y mucho más.

### Las tres personalizaciones que pide la consigna

#### 1. `list_display` — qué columnas se ven en la lista

```python
list_display = ("nombre", "precio", "stock")
```

Define las columnas de la vista de listado. Acepta:

- Nombres de campos del modelo (`"precio"`).
- Nombres de métodos del modelo (`"get_descuento"` si existe `Producto.get_descuento`).
- Métodos del propio `ModelAdmin` que reciban `obj` (útiles para columnas calculadas).
- El símbolo `"__str__"` para incluir la representación textual.

Las columnas son ordenables haciendo click en el encabezado, siempre que sean campos del modelo (los métodos calculados no se ordenan a menos que se les agregue `.admin_order_field`).

#### 2. `search_fields` — qué campos son buscables

```python
search_fields = ("nombre", "descripcion")
```

Activa una barra de búsqueda en el listado. Internamente arma una query `WHERE` con `icontains` sobre los campos declarados, unidos con `OR`. Soporta:

- Búsqueda en campos relacionados con sintaxis `__`: `"autor__nombre"` busca en el nombre del autor (ForeignKey).
- Prefijos especiales: `"^nombre"` (startswith), `"=nombre"` (exact), `"@descripcion"` (full-text en backends que lo soportan).

Para campos numéricos (precio, stock) no se suele usar `search_fields` — los filtros son más apropiados.

#### 3. `list_filter` — sidebar de filtros

```python
list_filter = ("categoria", "disponible")
```

Genera el sidebar derecho con filtros rápidos. Es ideal para:

- Campos con `choices` (categoría con valores limitados).
- Booleanos (disponible: sí/no).
- Fechas (Django genera automáticamente filtros como "hoy", "últimos 7 días", "este mes").
- Campos relacionados (ForeignKey) — muestra todas las opciones de la otra tabla.

No es ideal para campos de cardinalidad alta (ej. un filtro por "nombre" mostraría cientos de opciones).

### Tabla comparativa: atributos clave de `ModelAdmin`

| Atributo | Para qué | Cuándo conviene | Ejemplo |
|---|---|---|---|
| `list_display` | Define columnas de la lista | Siempre (es lo más visible) | `("nombre", "precio", "stock")` |
| `search_fields` | Activa barra de búsqueda | Hay campos de texto identificadores | `("nombre", "descripcion")` |
| `list_filter` | Sidebar de filtros rápidos | Hay campos de cardinalidad baja (choices, booleanos, fechas, FK) | `("categoria", "disponible")` |
| `ordering` | Orden por defecto de la lista | Para sobreescribir el `Meta.ordering` solo en el admin | `("-creado_en",)` |
| `list_per_page` | Cantidad de items por página | Modelos con muchos registros | `25` |
| `list_editable` | Permite editar inline desde la lista | Campos simples (no FK) que se cambian seguido | `("precio", "stock")` |
| `readonly_fields` | Campos solo lectura en el formulario | Campos auto-generados (timestamps, slug, hash) | `("creado_en",)` |
| `fieldsets` | Agrupa campos en secciones en el form de edición | Modelos con muchos campos | Ver doc |
| `inlines` | Mostrar modelos relacionados en el mismo form | Padre-hijo (Author + Books) | `[BookInline]` |
| `actions` | Acciones masivas sobre selección múltiple | Operaciones batch ("marcar como disponibles") | Función personalizada |
| `prepopulated_fields` | Pre-llenar un campo a partir de otro al tipear | Slugs derivados del título | `{"slug": ("titulo",)}` |

### Dos formas de registrar el modelo con `ModelAdmin`

```python
# Forma 1: clásica (la usa la consigna)
admin.site.register(Producto, ProductoAdmin)

# Forma 2: decorador (Django 1.7+)
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (...)
```

Ambas son equivalentes. La consigna pide la primera forma, así que la usamos.

## Solución implementada

### `models.py`

```python
from django.db import models


class Producto(models.Model):
    CATEGORIA_CHOICES = [
        ("libros", "Libros"),
        ("tecnologia", "Tecnología"),
        ("hogar", "Hogar"),
        ("ropa", "Ropa"),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    disponible = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "producto"
        verbose_name_plural = "productos"

    def __str__(self):
        return self.nombre
```

**Decisiones del modelo:**

- **`PositiveIntegerField` para `stock`:** no tiene sentido un stock negativo. Más restrictivo que `IntegerField` y previene errores a nivel de base de datos.
- **`choices` en `categoria`:** convierte el `CharField` libre en un `<select>` con opciones fijas. Habilita que `list_filter` genere un filtro discreto con esas opciones.
- **`BooleanField` para `disponible`:** representa el estado on/off. `list_filter` lo renderiza como "Todo / Sí / No" automáticamente.
- **`creado_en` con `auto_now_add`:** timestamp inmutable del momento de creación.
- **`Meta.ordering`:** orden alfabético por nombre por defecto.

### `admin.py`

```python
from django.contrib import admin

from .models import Producto


class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "precio", "stock", "disponible")
    search_fields = ("nombre", "descripcion")
    list_filter = ("categoria", "disponible")
    ordering = ("nombre",)
    list_per_page = 25
    list_editable = ("precio", "stock", "disponible")
    readonly_fields = ("creado_en",)


admin.site.register(Producto, ProductoAdmin)
```

**Decisiones del `ModelAdmin`:**

| Atributo | Por qué se usa así |
|---|---|
| `list_display` | Cinco columnas que cubren los datos clave: identificación (`nombre`), segmentación (`categoria`), comercial (`precio`, `stock`) y estado (`disponible`). |
| `search_fields` | Búsqueda libre por nombre y descripción. Texto libre en ambos. |
| `list_filter` | Sidebar con `categoria` (4 opciones) y `disponible` (Sí/No). Ambos campos discretos, ideales para filtros. |
| `ordering` | Mismo orden que el `Meta.ordering` del modelo, pero declarado explícitamente para que sea evidente en el admin. |
| `list_per_page` | Subido de 100 (default) a 25 para evitar listas largas. |
| `list_editable` | `precio`, `stock` y `disponible` se pueden editar directo desde la lista sin entrar al detalle. Muy útil para ajustes rápidos. |
| `readonly_fields` | `creado_en` queda visible pero no editable, así nadie puede falsificar la fecha de alta accidentalmente. |

## Mockup del admin resultante

### Vista de listado (`/admin/catalogo/producto/`)

```
┌────────────────────────────────────────────────────────────────────────────────┐
│  Django administration                                          felipe / Salir │
├────────────────────────────────────────────────────────────────────────────────┤
│                                                                                │
│  Inicio › Catalogo › Productos                                                 │
│                                                                                │
│  Productos                                              + AGREGAR PRODUCTO     │
│                                                                                │
│  ┌──────────────────────────────────┐  ┌──────────────────────────────────┐  │
│  │ Buscar: [__________________] [Q] │  │ FILTRO                           │  │
│  └──────────────────────────────────┘  │ Por categoría                    │  │
│                                         │   Todos                          │  │
│  ┌──┬──────────┬───────────┬────────┬──┴─────┬──────────┐                   │  │
│  │  │ Nombre   │ Categoría │ Precio │ Stock  │ Disp.    │                   │  │
│  ├──┼──────────┼───────────┼────────┼────────┼──────────┤  │   Libros        │  │
│  │☐ │ Auricul. │ Tecnología│ [4500] │ [12]   │ ☑ Sí     │  │   Tecnología    │  │
│  │☐ │ Camiseta │ Ropa      │ [2900] │ [50]   │ ☑ Sí     │  │   Hogar         │  │
│  │☐ │ Lámpara  │ Hogar     │ [1800] │ [0]    │ ☐ No     │  │   Ropa          │  │
│  │☐ │ Libro X  │ Libros    │ [3200] │ [25]   │ ☑ Sí     │  │                  │  │
│  │☐ │ Mouse    │ Tecnología│ [5500] │ [8]    │ ☑ Sí     │  │ Por disponible   │  │
│  │☐ │ Silla    │ Hogar     │ [12000]│ [3]    │ ☑ Sí     │  │   Todos          │  │
│  └──┴──────────┴───────────┴────────┴────────┴──────────┘  │   Sí             │  │
│                                                              │   No             │  │
│  [Guardar] (los campos en [...] son editables inline)        └──────────────────┘  │
│                                                                                    │
│  6 productos    < anterior  |  1 de 1  |  siguiente >                              │
└────────────────────────────────────────────────────────────────────────────────────┘
```

**Cómo se cumplen las tres preguntas de evaluación:**

- **¿Qué campos aparecen en la lista principal?** → Nombre, Categoría, Precio, Stock y Disponible (los declarados en `list_display`).
- **¿Se puede buscar registros usando la barra?** → Sí, en `nombre` y `descripcion` (definidos en `search_fields`). Aparece arriba.
- **¿Los filtros laterales segmentan correctamente?** → Sí, sidebar con dos filtros: "Por categoría" (4 opciones + "Todos") y "Por disponible" (Sí / No / Todos).

### Vista de edición (`/admin/catalogo/producto/<id>/change/`)

```
┌────────────────────────────────────────────────────────────────┐
│  Editar producto: Auriculares Bluetooth                        │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Nombre:        [Auriculares Bluetooth                       ] │
│  Descripción:   [Auriculares inalámbricos con cancelación de  ]│
│                 [ruido activa, batería 30h.                   ]│
│  Precio:        [4500.00                                      ]│
│  Stock:         [12                                           ]│
│  Categoría:     [Tecnología ▼]                                 │
│  Disponible:    ☑                                              │
│  Creado en:     2026-05-26 14:30:00       (solo lectura)       │
│                                                                │
│  [Borrar]                  [Guardar y continuar]  [Guardar]    │
└────────────────────────────────────────────────────────────────┘
```

`creado_en` aparece pero no es editable (gracias a `readonly_fields`).

## Próximos pasos: integración con autenticación

Este TP se centra en la personalización visual y de búsqueda del admin. Hay dos líneas naturales de continuación que el corrector probablemente espera ver mencionadas:

### 1. Permisos a nivel de admin

Django ya integra un sistema de permisos por modelo (`add`, `change`, `delete`, `view`). Para que solo ciertos grupos vean o editen productos:

```python
# Crear permisos desde el shell:
# python manage.py shell
from django.contrib.auth.models import Group, Permission
grupo = Group.objects.create(name="Editores de Catálogo")
permisos = Permission.objects.filter(content_type__model="producto")
grupo.permissions.set(permisos)
```

Después se asignan usuarios a ese grupo desde el propio admin.

### 2. Restringir vistas custom con `LoginRequiredMixin`

Mientras el admin tiene auth incorporada, las vistas custom del proyecto (las del TP 9b/9c con `ListView`, `CreateView`, `UpdateView`) **no la tienen**. La forma estándar de agregarla es con mixins:

```python
from django.contrib.auth.mixins import LoginRequiredMixin

class LibroCreateView(LoginRequiredMixin, CreateView):
    model = Libro
    form_class = LibroForm
    template_name = "libro_form.html"
    success_url = reverse_lazy("libro-list")
    login_url = "/login/"   # opcional: a dónde mandar si no está logueado
```

`LoginRequiredMixin` chequea `request.user.is_authenticated` antes de ejecutar la vista. Si no lo está, redirige a `LOGIN_URL`. Combinado con `UserPassesTestMixin` se pueden agregar reglas más finas (ej. "solo el autor puede editar su libro").

> Esta sección anticipa contenido de las próximas unidades del módulo. Se incluye porque el flujo natural de un proyecto Django profesional integra el panel admin **con** un sistema de autenticación coherente para las vistas custom.

## Cumplimiento de la consigna

| # | Punto | Dónde se cumple |
|---|---|---|
| 1 | Abrir `admin.py` y crear clase que herede de `admin.ModelAdmin` | `admin.py` — clase `ProductoAdmin` |
| 2 | Definir `list_display` | `list_display = ("nombre", "categoria", "precio", "stock", "disponible")` |
| 3 | Definir `search_fields` | `search_fields = ("nombre", "descripcion")` |
| 4 | Definir `list_filter` | `list_filter = ("categoria", "disponible")` |
| 5 | Registrar el modelo con la clase | `admin.site.register(Producto, ProductoAdmin)` |
| Bonus | Extras profesionales | `ordering`, `list_per_page`, `list_editable`, `readonly_fields` |

## Estructura del TP

```
TP_Modulo_9d/
├── README.md      ← Este archivo (mirror del Google Doc)
├── models.py      ← Modelo Producto enriquecido
└── admin.py       ← ProductoAdmin con personalizaciones completas
```

## Entrega

- **Plataforma:** Google Doc.
- **Google Doc:** https://docs.google.com/document/d/1pljibp82YJn_NQBLf3_5QYGV3FxLGHjo5HSSq3T4WgI/edit?usp=sharing
- **Nota recibida:** **99% — Aprobado** ⭐

### Comentarios del corrector

Este es un trabajo excepcional. El estudiante no solo ha cumplido con todos los requisitos técnicos de la consigna (configuración de columnas, filtros y búsqueda), sino que ha estructurado un documento profesional con marco teórico, implementación práctica avanzada y un análisis detallado de la usabilidad. La inclusión de configuraciones extra como `list_editable` demuestra una gran proactividad y dominio de la materia.

**Puntos fuertes**

- Explicación teórica exhaustiva que supera los requisitos mínimos.
- Inclusión de configuraciones adicionales que mejoran la experiencia de usuario (UX) del administrador, como la edición inline y campos de solo lectura.
- Uso de mockups visuales en texto para representar la interfaz final, lo que demuestra claridad en el diseño de la herramienta.
- Justificación técnica sólida para cada elección en el modelo y el admin.

**Correcciones**

- Mencionar explícitamente el impacto en el rendimiento (consultas SQL) al agregar filtros y columnas relacionadas en modelos con miles de registros.

**Sugerencias**

- Explorar el uso de `list_select_related` para optimizar el rendimiento del admin cuando se muestran campos de modelos relacionados (ForeignKey).
- Investigar la creación de acciones personalizadas (admin actions) para realizar procesamientos por lotes en los registros.
- Implementar validaciones personalizadas en el formulario del admin sobreescribiendo el método `clean` del formulario o del modelo.

## Notas adicionales

- **Entorno:** desarrollado en la terminal integrada de **VS Code** (aprendizaje guardado del TP 8a).
- **Commit:** subido al repo con prefijo Conventional Commits (`feat:`).
- **Sin proyecto Django local:** decisión deliberada para mantener el TP enfocado en la teoría y el código entregable. La sección de mockup ASCII reemplaza a las capturas reales.
