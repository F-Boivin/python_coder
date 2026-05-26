# TP Módulo 9 — Unidad 7: CreateView y UpdateView (CBV)

Trabajo práctico de la Unidad 7 del Módulo 9 del curso de Python de Coderhouse. Autograder en el editor online de Coder.

## Consigna

Implementar `CreateView` y `UpdateView` de Django para gestionar la creación y edición de objetos del modelo `Libro` desde el frontend. Incluye:

- Modelo `Libro` (provisto por la consigna).
- `ModelForm` (`LibroForm`) que mapea los tres campos.
- Dos vistas basadas en clases con `success_url` y opcionalmente `form_valid`.
- URLs con captura de `pk` para la edición.
- Template `libro_form.html` reutilizable para crear y editar.

## Marco teórico

### `CreateView` y `UpdateView` — qué hacen

Son dos vistas genéricas de `django.views.generic.edit` que implementan el patrón **"mostrar formulario en GET, procesar en POST"** automáticamente:

| Aspecto | `CreateView` | `UpdateView` |
|---------|--------------|--------------|
| Qué hace | Crea una instancia nueva del modelo | Edita una instancia existente |
| Cómo identifica el objeto | No aplica — crea uno nuevo | `pk` o `slug` desde la URL |
| Formulario inicial | Vacío | Pre-cargado con los datos actuales |
| Atributos clave | `model`, `form_class`, `template_name`, `success_url` | Idem `CreateView` |
| Template default | `<app>/<modelo>_form.html` | Idem |

Comparten la mayoría de la configuración, por eso típicamente usan **el mismo template** (`libro_form.html`) — distinguen el modo con `{% if object %}` en el HTML.

### `ModelForm` — por qué usarlo

Un `ModelForm` deriva los campos del formulario directamente del modelo. Ventajas:

- **No duplicación:** los campos los declarás una sola vez en el modelo.
- **Validación gratis:** los tipos de campo y restricciones (`max_length`, `blank`, etc.) se traducen automáticamente a validaciones.
- **Guardado automático:** `form.save()` crea o actualiza la instancia.

Alternativa: usar `Form` plano y mapear manualmente, pero implica reescribir lo que ya está en el modelo.

### `success_url` con `reverse_lazy`

Después de un `form.save()` exitoso, la vista redirige a `success_url`. Hay dos formas de definirlo:

- `success_url = '/libros/'` — hardcoded, no recomendado.
- `success_url = reverse_lazy('libro-list')` — usa el `name` del URL pattern, sobrevive a refactorings.

Es **`reverse_lazy`** y no `reverse` porque el URL pattern no está resuelto aún cuando se carga la clase (las URLs se evalúan después que se importen las vistas). `reverse_lazy` posterga la resolución hasta el momento del uso.

### `form_valid()` — hook para lógica custom

Es el método que `CreateView`/`UpdateView` llaman cuando el form pasa todas las validaciones. La implementación base hace `form.save()` y redirige. Sobreescribirlo permite agregar lógica antes o después de guardar:

```python
def form_valid(self, form):
    form.instance.autor = self.request.user   # asignar usuario actual
    return super().form_valid(form)
```

En este TP la lógica base alcanza (no hay datos custom para asignar), pero implementamos el método explícitamente porque demuestra que conocemos el hook (y porque el material teórico lo incluye).

### Reutilizar template entre Create y Update

El mismo `libro_form.html` sirve para ambos casos. Para distinguirlos en el HTML:

```django
<h2>{% if object %}Editar Libro{% else %}Nuevo Libro{% endif %}</h2>
```

- En `UpdateView`, `object` está poblado con la instancia que se está editando → muestra "Editar".
- En `CreateView`, `object` es `None` → muestra "Nuevo".

Esto es DRY al máximo: una sola plantilla, dos modos.

## Solución implementada

### `models.py`

```python
from django.db import models

class Libro(models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.titulo
```

Provisto por la consigna, sin cambios.

### `forms.py`

```python
from django import forms
from .models import Libro

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'descripcion']
```

`ModelForm` mínimo. La clase `Meta` declara el modelo y los campos a exponer.

### `views.py`

```python
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from .models import Libro
from .forms import LibroForm


class LibroCreateView(CreateView):
    model = Libro
    form_class = LibroForm
    template_name = 'libro_form.html'
    success_url = reverse_lazy('libro-list')

    def form_valid(self, form):
        return super().form_valid(form)


class LibroUpdateView(UpdateView):
    model = Libro
    form_class = LibroForm
    template_name = 'libro_form.html'
    success_url = reverse_lazy('libro-list')

    def form_valid(self, form):
        return super().form_valid(form)
```

Decisiones:
- `form_class = LibroForm` (no `fields = [...]`) porque permite reusar el `ModelForm` si se enriquece más adelante.
- `template_name = 'libro_form.html'` — mismo template en ambas vistas.
- `form_valid()` implementado aunque sin lógica extra (solo `super()`) — sirve como punto de extensión documentado.

### `urls.py`

```python
from django.urls import path
from .views import LibroCreateView, LibroUpdateView

urlpatterns = [
    path('libro/nuevo/', LibroCreateView.as_view(), name='libro-create'),
    path('libro/<int:pk>/editar/', LibroUpdateView.as_view(), name='libro-update'),
]
```

### `templates/libro_form.html`

```django
{% extends 'base.html' %}

{% block content %}
    <h2>{% if object %}Editar Libro{% else %}Nuevo Libro{% endif %}</h2>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Guardar</button>
    </form>
{% endblock %}
```

Tres detalles importantes:
- **`{% extends 'base.html' %}`** asume que existe un `base.html` en el proyecto (template base con `<html>`, `<head>`, `<body>` y un `{% block content %}`).
- **`{% csrf_token %}`** es obligatorio en cualquier `<form method="post">` en Django, sino tira 403.
- **`{{ form.as_p }}`** renderiza el formulario con cada campo envuelto en un `<p>` — la forma más rápida de generar el HTML.

## Estructura del TP

```
TP_Modulo_9c/
├── README.md
├── models.py
├── forms.py
├── views.py
├── urls.py
└── templates/
    └── libro_form.html
```

## Cumplimiento de la consigna

| # | Punto | Dónde se cumple |
|---|-------|-----------------|
| 1 | Definir modelo `Libro` | `models.py` |
| 2 | Crear `ModelForm` (opcional pero recomendado) | `forms.py` |
| 3 | Implementar `CreateView` y `UpdateView` | `views.py` |
| 4 | Configurar URLs | `urls.py` |
| 5 | Crear template `libro_form.html` | `templates/libro_form.html` |
| Extra | `form_valid()` aunque sin lógica custom | Método declarado en ambas vistas |

## Entrega

- **Plataforma:** editor online de Coder con autograder (IA).
- **Nota recibida:** **100% — Excelente** 🎯

### Comentarios del corrector

El código enviado es excelente y cumple con todos los requisitos del ejercicio. Has implementado las vistas genéricas de Django siguiendo las mejores prácticas, configurando correctamente los formularios, las rutas y la reutilización de plantillas.

**Puntos fuertes**

- Implementación precisa de vistas basadas en clases (CBV).
- Uso correcto de `reverse_lazy` para la redirección exitosa.
- Reutilización eficiente de plantillas con lógica condicional.
- Configuración adecuada y segura (CSRF) del formulario HTML.

**Correcciones**

El código es muy limpio y funcional. No requiere correcciones, pero se podría explorar el uso de **mixins** si en el futuro se necesitan validaciones personalizadas más complejas en las vistas.

**Próximos pasos sugeridos**

- Agregar validación de permisos (ej. `LoginRequiredMixin`) para asegurar que solo usuarios autorizados puedan crear o editar libros. **⚠️ Segunda mención consecutiva del corrector — anticipar este patrón en el próximo TP de Django.**
- Implementar un `DeleteView` para completar el CRUD de libros.

## Notas adicionales

- **Aprendizajes aplicados** del 9a (limpiar TODOs) y del 9b (`context_object_name` explícito) — consistentemente sumaron al puntaje.
- **Entorno:** desarrollado en la terminal integrada de **VS Code**.
- **Commit:** `feat:` con Conventional Commits.
