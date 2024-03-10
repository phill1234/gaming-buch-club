"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import logging
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
import dj_database_url

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

BASE_DIR = Path(__file__).resolve().parent.parent

PROJECT_NAME = "Gaming Buch Club"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-x78=*z7!97h84504qv70$4@*r)jp=r2=)ch#^v7w9&nu4gbsqs"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if os.getenv("PRODUCTION") else True

ENVIRONMENT = os.getenv("ENVIRONMENT", "local")

ALLOWED_HOSTS = ["backend.gamingbuchclub.de", "gamingbuchclub.de"]

if DEBUG:
    ALLOWED_HOSTS.extend(["localhost", "0.0.0.0", "127.0.0.1"])

database_url_for_local_development = ""
if not os.getenv("DATABASE_URL"):
    import docker_database_url

    database_url_for_local_development = docker_database_url.start_db_and_get_url(
        db_name="gaming_book_club_backend", database_url_name="DATABASE_URL"
    )
default_database_url = os.getenv(
    "DATABASE_URL",
    database_url_for_local_development,
)
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "blog",
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

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "project.wsgi.application"

CSRF_TRUSTED_ORIGINS = ["https://gamingbuchclub.de", "https://*.gamingbuchclub.de"]

DATABASES = {
    "default": dj_database_url.parse(default_database_url),
}

sentry_logging = LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)
if not DEBUG:
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        environment=ENVIRONMENT,
        integrations=[sentry_logging, DjangoIntegration()],
    )

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CACHE_URL = os.getenv("CACHE_URL", "redis://redis:6379/1")
if DEBUG:
    CACHE_URL = "redis://localhost:6379/1"
