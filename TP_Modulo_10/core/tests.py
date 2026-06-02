"""Tests smoke para la app core."""

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Author, Post, Tag


class ModelTests(TestCase):
    def test_author_str(self):
        autor = Author.objects.create(name="Ada Lovelace", email="ada@example.com")
        self.assertEqual(str(autor), "Ada Lovelace")

    def test_post_clean_rechaza_titulo_corto(self):
        autor = Author.objects.create(name="Autor", email="a@example.com")
        post = Post(title="abc", content="x", published_date=timezone.now(), author=autor)
        with self.assertRaises(ValidationError):
            post.clean()

    def test_post_clean_acepta_titulo_valido(self):
        autor = Author.objects.create(name="Autor", email="b@example.com")
        post = Post(title="Título válido", content="x", published_date=timezone.now(), author=autor)
        post.clean()  # no debe levantar excepción


class ViewTests(TestCase):
    def setUp(self):
        self.autor = Author.objects.create(name="Autor", email="c@example.com")
        self.post = Post.objects.create(
            title="Post publicado",
            content="contenido",
            published_date=timezone.now(),
            author=self.autor,
        )

    def test_post_list_muestra_publicados(self):
        response = self.client.get(reverse("core:post-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Post publicado")

    def test_post_futuro_no_aparece(self):
        Post.objects.create(
            title="Post del futuro",
            content="aún no",
            published_date=timezone.now() + timezone.timedelta(days=30),
            author=self.autor,
        )
        response = self.client.get(reverse("core:post-list"))
        self.assertNotContains(response, "Post del futuro")
