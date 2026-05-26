# TP Módulo 9 — Unidades 4-6: Vistas, CBV, ListView y DetailView

Trabajo práctico que cubre las Unidades 4, 5 y 6 del Módulo 9 del curso de Python de Coderhouse. Es un autograder en el editor online de Coder.

> Este README consolida también la teoría de las Unidades 4 y 5 aunque no tengan entrega propia, porque conforman el contexto necesario para entender la Unidad 6 (que sí tiene autograder).

## Consigna

El editor online de Coder presenta el código de cinco archivos en un solo documento:

- `models.py` — modelo `Libro` ya definido.
- `views.py` — imports listos + TODO para implementar `LibroListView` y `LibroDetailView`.
- `urls.py` — imports listos + TODO para añadir las rutas.
- `templates/libros/lista_libros.html` — TODO para crear la plantilla de lista.
- `templates/libros/detalle_libro.html` — TODO para crear la plantilla de detalle.

Hay que completar los cuatro TODO usando vistas basadas en clases (CBV) genéricas de Django.

## Marco teórico

### Unidad 4 — Vistas y plantillas con FBV

Una **vista basada en función (FBV)** es una función Python que recibe un `request` y devuelve un `HttpResponse`. Para listar objetos, un patrón típico es:

```python
def lista_objetos(request):
    objetos = TuModelo.objects.all()
    return render(request, 'app/lista_objetos.html', {'objetos': objetos})
```

Las FBV son simples y directas, ideales para vistas con poca lógica común. Pero cuando hay muchas operaciones CRUD repetidas (listar, ver detalle, crear, editar, borrar), el código se vuelve redundante.

### Unidad 5 — CBV: ¿Por qué y cuándo usarlas?

Una **vista basada en clase (CBV)** encapsula la lógica en una clase Python que hereda de una vista genérica de Django (`ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`). Esto permite reutilizar el patrón sin reescribir el código.

**FBV vs CBV — comparativa:**

| Aspecto | FBV | CBV |
|---------|-----|-----|
| Forma | Función Python | Clase que hereda de una vista genérica |
| Lógica | Explícita y plana | Inferida del patrón genérico, customizable con atributos/métodos |
| Reutilización | Baja (copy-paste para casos similares) | Alta (herencia y mixins) |
| Curva de aprendizaje | Inmediata | Media (hay que conocer la jerarquía de clases genéricas) |
| Caso ideal | Vistas únicas con lógica particular | CRUD repetitivo, listados, formularios estándar |
| Ejemplo equivalente | `def lista(request): productos = Producto.objects.all(); return render(...)` | `class ProductoListView(ListView): model = Producto` |

**Las cinco CBV genéricas de Django:**

- `ListView` — listado de objetos de un modelo.
- `DetailView` — detalle de un objeto específico (recibe `pk` o `slug` desde la URL).
- `CreateView` — formulario para crear un nuevo objeto.
- `UpdateView` — formulario para editar uno existente.
- `DeleteView` — confirmación + borrado.

Las tres últimas (`Create`, `Update`, `Delete`) usan `ModelForm` internamente y se cubren en módulos posteriores.

### Unidad 6 — ListView y DetailView en práctica

**`ListView`** recibe un modelo y automáticamente:

1. Hace `Modelo.objects.all()` para obtener el queryset.
2. Pasa ese queryset al template bajo el nombre `object_list` (o el nombre que se indique en `context_object_name`).
3. Renderiza el template indicado en `template_name`.

**`DetailView`** recibe un modelo y un identificador (`pk` o `slug`) desde la URL, y automáticamente:

1. Busca `Modelo.objects.get(pk=pk_de_la_url)`.
2. Si no existe, devuelve un 404.
3. Pasa el objeto al template como `object` (o `context_object_name`).

Por eso una CBV bien escrita son ~4 líneas que reemplazan ~10-15 líneas de una FBV equivalente.

## Solución implementada

### `views.py`

```python
from django.views.generic import ListView, DetailView

from .models import Libro


class LibroListView(ListView):
    model = Libro
    template_name = 'libros/lista_libros.html'
    context_object_name = 'libros'


class LibroDetailView(DetailView):
    model = Libro
    template_name = 'libros/detalle_libro.html'
    context_object_name = 'libro'
```

Decisión sobre `context_object_name`: los templates referencian `libros` (en el `{% for libro in libros %}`) y `libro` (en `{{ libro.titulo }}`). Esos nombres tienen que coincidir, por eso se setean explícitamente. Sin esto, los defaults serían `object_list` y `object`.

### `urls.py`

```python
from django.urls import path

from .views import LibroListView, LibroDetailView


urlpatterns = [
    path('libros/', LibroListView.as_view(), name='lista_libros'),
    path('libros/<int:pk>/', LibroDetailView.as_view(), name='detalle_libro'),
]
```

Decisiones clave:
- **`.as_view()`** convierte la clase en una función llamable por Django. Es obligatorio en CBV.
- **`<int:pk>`** captura un entero de la URL y se lo pasa a `DetailView` como el `pk` para buscar el objeto.
- **`name='lista_libros'`** y `'detalle_libro'` son los nombres usados por los templates en `{% url ... %}` para construir links sin hardcodear paths.

### `templates/libros/lista_libros.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Lista de Libros</title>
</head>
<body>
    <h1>Lista de Libros</h1>
    <ul>
        {% for libro in libros %}
            <li><a href="{% url 'detalle_libro' libro.pk %}">{{ libro.titulo }}</a> - {{ libro.autor }}</li>
        {% empty %}
            <li>No hay libros disponibles.</li>
        {% endfor %}
    </ul>
</body>
</html>
```

Uso de tres tags clave del template language:
- `{% for libro in libros %}` itera el queryset que pasó la `ListView`.
- `{% empty %}` muestra contenido alternativo si el queryset está vacío (mucho más limpio que un `{% if libros %}` envolviendo todo).
- `{% url 'detalle_libro' libro.pk %}` construye la URL al detalle pasando el `pk` como argumento posicional.

### `templates/libros/detalle_libro.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Detalle del Libro</title>
</head>
<body>
    <h1>{{ libro.titulo }}</h1>
    <p><strong>Autor:</strong> {{ libro.autor }}</p>
    <p><strong>Fecha de publicación:</strong> {{ libro.fecha_publicacion }}</p>
    <a href="{% url 'lista_libros' %}">Volver a la lista</a>
</body>
</html>
```

Navegación bidireccional con el enlace de "Volver a la lista" — buena práctica de UX.

## Estructura del TP

```
TP_Modulo_9b/
├── README.md
├── models.py                          ← Modelo Libro (provisto por la consigna)
├── views.py                           ← LibroListView + LibroDetailView
├── urls.py                            ← Rutas para ambas vistas
└── templates/
    └── libros/
        ├── lista_libros.html
        └── detalle_libro.html
```

## Conceptos aplicados por unidad

| Unidad | Concepto | Dónde aparece |
|--------|----------|---------------|
| U4 — FBV | Patrón function-based view, render con contexto | Marco teórico (no se usa en código porque la consigna pide CBV) |
| U5 — Comparativa FBV vs CBV | Cuándo usar cada una, ventajas de las clases genéricas | Marco teórico + tabla comparativa |
| U6 — ListView y DetailView | CBV genéricas, `template_name`, `context_object_name`, `.as_view()`, `<int:pk>` | `views.py` y `urls.py` |

## Cumplimiento de la consigna

| # | TODO de la consigna | Dónde se cumple |
|---|---------------------|-----------------|
| 1 | Implementar `LibroListView` y `LibroDetailView` | `views.py` |
| 2 | Añadir rutas para las vistas | `urls.py` |
| 3 | Crear plantilla para mostrar lista de libros | `templates/libros/lista_libros.html` |
| 4 | Crear plantilla para mostrar detalle de un libro | `templates/libros/detalle_libro.html` |

## Entrega

- **Plataforma:** editor online de Coder con autograder (IA).
- **Nota recibida:** **100% — Excelente** 🎯

### Comentarios del corrector

El estudiante ha realizado una implementación excelente y completa de `ListView` y `DetailView` en Django. El código propuesto cumple con todas las expectativas funcionales y de estructuración del ejercicio sin presentar errores.

**Puntos fuertes**

- Implementación precisa de vistas basadas en clases siguiendo las convenciones de Django.
- Uso correcto y seguro de etiquetas de plantillas como `{% url %}` y el condicional `{% empty %}`.
- Navegación bidireccional clara y funcional entre la lista de elementos y el detalle de los mismos.
- Código limpio, legible y bien estructurado.

**Correcciones**

El código es excelente; no se requieren mejoras funcionales. Podría profundizar explorando cómo agregar paginación a la `ListView` o cómo manejar errores 404 de forma personalizada si el objeto no existe.

**Próximos pasos sugeridos**

- Investigar sobre **mixins** en Django para añadir lógica de autenticación a las vistas (por ejemplo, `LoginRequiredMixin`).
- Practicar la creación de formularios con `CreateView` y `UpdateView` para permitir la gestión de los datos desde el frontend.

## Notas adicionales

- **Aprendizaje aplicado del TP 9a (99%):** se eliminaron los comentarios `# TODO` del código pre-cargado antes de entregar. Ese era el único punto que costó 1% en el TP anterior. Resultado: 100%.
- **Entorno:** desarrollado en la terminal integrada de **VS Code**.
- **Commit:** subido al repo con prefijo Conventional Commits (`feat:`).
