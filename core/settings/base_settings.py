import os
from pathlib import Path
from typing import Any

from decouple import config

BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

SECRET_KEY: str = config("SECRET_KEY")

DEBUG: bool = config("DEBUG", cast=bool, default=False)

ALLOWED_HOSTS: list[str] = ["*"]

INSTALLED_APPS: list[str] = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.github",
    "crispy_forms",
    "crispy_bootstrap4",
    "accounts",
]

MIDDLEWARE: list[str] = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF: str = "core.urls"

TEMPLATES: list[dict[str, Any]] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "./templates")],
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

WSGI_APPLICATION: str = "core.wsgi.application"

DEFAULT_AUTO_FIELD: str = "django.db.models.BigAutoField"

AUTH_PASSWORD_VALIDATORS: list[dict[str, str]] = [
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

AUTH_USER_MODEL: str = "accounts.CustomUser"

LANGUAGE_CODE: str = "en-us"

TIME_ZONE: str = "UTC"

USE_I18N: bool = True

USE_TZ: bool = True

STATIC_URL: str = "/static/"
STATICFILES_DIRS: tuple[str, ...] = (str(BASE_DIR.joinpath("static")),)
STATIC_ROOT: str = str(BASE_DIR.joinpath("staticfiles"))
STATICFILES_FINDERS: list[str] = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
STORAGES: dict[str, dict[str, str]] = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

AUTHENTICATION_BACKENDS: tuple[str, ...] = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

SITE_ID: int = 1

ACCOUNT_EMAIL_VERIFICATION: str = "none"

LOGIN_REDIRECT_URL: str = "home"
LOGOUT_REDIRECT_URL: str = "home"

SOCIALACCOUNT_PROVIDERS: dict[str, dict[str, Any]] = {
    "github": {
        "SCOPE": [
            "user",
            "repo",
            "read:org",
        ],
        "APP": {
            "client_id": config("GH_CLIENT_ID", default=""),
            "secret": config("GH_CLIENT_SECRET", default=""),
        },
    }
}

CRISPY_ALLOWED_TEMPLATE_PACKS: str = "bootstrap4"
CRISPY_TEMPLATE_PACK: str = "bootstrap4"
