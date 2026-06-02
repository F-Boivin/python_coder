"""Configuración del proyecto biblioteca.

TP final del Módulo 9 del curso de Python de Coderhouse.
Configurado para desarrollo local con SQLite, autenticación por defecto y
templates compartidos en el directorio raíz.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Seguridad (configuración de desarrollo) ---
# En un proyecto de producción, SECRET_KEY y DEBUG deberían venir de
# variables de entorno. Para este TP de desarrollo se dejan en el código.
SECRET_KEY = "django-insecure-tp-final-modulo-9-coder-2026-no-usar-en-prod"
DEBUG = True
ALLOWED_HOSTS = ["*"]

# --- Aplicaciones ---
INSTALLED_APPS = [
    # Apps de Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Apps del proyecto
    "catalogo",
    "usuarios",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "biblioteca.urls"

# --- Templates ---
# Carpeta `templates/` en la raíz contiene base.html y las subcarpetas
# `catalogo/` y `usuarios/` con los templates de cada app.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "biblioteca.wsgi.application"

# --- Base de datos: SQLite por defecto ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# --- Validación de contraseñas ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Internacionalización ---
LANGUAGE_CODE = "es-ar"
TIME_ZONE = "America/Argentina/Buenos_Aires"
USE_I18N = True
USE_TZ = True

# --- Archivos estáticos ---
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# --- Tipo de PK por defecto ---
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Configuración de autenticación ---
# Estas URLs son las que Django usa para redirigir después de login, logout
# y cuando un LoginRequiredMixin bloquea una vista a un usuario anónimo.
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "libro-list"
LOGOUT_REDIRECT_URL = "libro-list"
