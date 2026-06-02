"""Vistas CRUD para Post usando Class-Based Views (Unidad 5).

- PostListView: lista los posts publicados (published_date <= ahora),
  ordenados por fecha descendente, con get_queryset personalizado y
  optimización de consultas.
- PostDetailView / PostCreateView / PostUpdateView / PostDeleteView:
  el resto del CRUD.
"""

from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import PostForm
from .models import Author, Post


class PostListView(ListView):
    model = Post
    template_name = "core/post_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        """Solo posts ya publicados, con autor y tags precargados.

        Filtra por published_date <= ahora (un post con fecha futura está
        'programado' y no se muestra todavía). select_related evita N+1 al
        acceder a post.author; prefetch_related hace lo propio con tags.
        """
        return (
            Post.objects.filter(published_date__lte=timezone.now())
            .select_related("author")
            .prefetch_related("tags")
            .order_by("-published_date")
        )


class PostDetailView(DetailView):
    model = Post
    template_name = "core/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return Post.objects.select_related("author").prefetch_related("tags")


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "core/post_form.html"
    success_url = reverse_lazy("core:post-list")


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "core/post_form.html"
    success_url = reverse_lazy("core:post-list")


class PostDeleteView(DeleteView):
    model = Post
    template_name = "core/post_confirm_delete.html"
    success_url = reverse_lazy("core:post-list")
    context_object_name = "post"


class AuthorDetailView(DetailView):
    """Detalle de un autor con la lista de sus publicaciones.

    Feature agregada en la rama feature/core-update (Unidad 9). Usa
    prefetch_related para traer todos los posts del autor en una sola
    query adicional, evitando el problema N+1 al iterarlos en el template.
    """

    model = Author
    template_name = "core/author_detail.html"
    context_object_name = "author"

    def get_queryset(self):
        return Author.objects.prefetch_related("posts")
