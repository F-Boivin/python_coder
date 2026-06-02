"""Tests básicos para el módulo catalogo.

No buscan cobertura exhaustiva — son smoke tests que validan que los
modelos se crean, las URLs resuelven y las vistas devuelven códigos
HTTP esperados según el estado de autenticación.
"""

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Autor, Libro


User = get_user_model()


class CatalogoModelTests(TestCase):
    def test_autor_str(self):
        autor = Autor.objects.create(nombre="Jorge Luis", apellido="Borges")
        self.assertEqual(str(autor), "Borges, Jorge Luis")

    def test_libro_str(self):
        autor = Autor.objects.create(nombre="Jorge Luis", apellido="Borges")
        libro = Libro.objects.create(
            titulo="Ficciones",
            autor=autor,
            fecha_publicacion="1944-01-01",
        )
        self.assertEqual(str(libro), "Ficciones")


class CatalogoViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.autor = Autor.objects.create(nombre="Julio", apellido="Cortázar")
        self.libro = Libro.objects.create(
            titulo="Rayuela",
            autor=self.autor,
            fecha_publicacion="1963-01-01",
        )

    def test_libro_list_publico(self):
        response = self.client.get(reverse("libro-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rayuela")

    def test_libro_create_requiere_login(self):
        response = self.client.get(reverse("libro-create"))
        # Debería redirigir al login (302)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/usuarios/login/", response.url)

    def test_libro_create_con_login(self):
        user = User.objects.create_user(username="tester", password="test1234!")
        self.client.login(username="tester", password="test1234!")
        response = self.client.get(reverse("libro-create"))
        self.assertEqual(response.status_code, 200)
