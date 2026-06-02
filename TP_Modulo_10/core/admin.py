"""Registro y personalización del admin para Author, Tag y Post.

Unidad 4: configura list_display y search_fields. Suma extras aprendidos
en módulos anteriores: list_filter, list_select_related y filter_horizontal
para la relación M2M.
"""

from django.contrib import admin

from .models import Author, Post, Tag


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "email")
    search_fields = ("name", "email")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_date")
    search_fields = ("title", "content")
    list_filter = ("published_date", "author", "tags")
    # Optimización: resuelve la FK author del listado con un JOIN
    list_select_related = ("author",)
    # Widget cómodo para la relación ManyToMany con Tag
    filter_horizontal = ("tags",)
    date_hierarchy = "published_date"
